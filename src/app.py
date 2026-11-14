"""APICN004 — Indian Income Tax RAG VoiceBot (Streamlit).

One screen, one RAG pipeline, four interaction modes:
    TITO  text  -> text        TIVO  text  -> voice
    VITO  voice -> text        VIVO  voice -> voice

Input (typed vs microphone) and output (text vs spoken) are chosen per mode; the
retrieval + grounded generation in `src.rag.core` is identical for all four.

Run:  streamlit run src/app.py
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

# Make `src.*` importable when Streamlit runs this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

from src.rag import core  # noqa: E402
from src.ui import components as ui  # noqa: E402


def _init_state() -> None:
    st.session_state.setdefault("history", [])  # list of {role, content, sources?}
    st.session_state.setdefault("last_audio_hash", None)
    st.session_state.setdefault("audio_key", 0)  # bumped to reset the mic after each turn


def _render_history() -> None:
    autoplay_idx = (
        len(st.session_state.history) - 1
        if st.session_state.pop("pending_autoplay", False)
        else -1
    )
    for i, turn in enumerate(st.session_state.history):
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])
            if turn.get("sources"):
                with st.expander("Sources"):
                    st.markdown(ui.format_sources(turn["sources"]))
            if turn.get("audio"):
                st.audio(
                    turn["audio"],
                    format=turn.get("audio_mime", "audio/mp3"),
                    autoplay=(i == autoplay_idx),
                )


def _get_retriever_or_warn():
    try:
        return core.get_retriever()
    except Exception as exc:  # noqa: BLE001
        st.error(
            f"Could not load the retrieval index: {exc}\n\n"
            "Build it first with:  `python src/rag/ingest.py`"
        )
        return None


def _handle_question(question: str, out_kind: str, will_rerun: bool = False) -> None:
    """Run the shared pipeline for one question and append the result to history."""
    st.session_state.history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        llm_history = ui.to_llm_history(st.session_state.history[:-1])
        try:
            sources, token_gen = core.stream_answer(question, history=llm_history)
            placeholder = st.empty()
            acc = ""
            for tok in token_gen:
                acc += tok
                placeholder.markdown(ui.latex_to_text(acc) + " ▌")
            answer = ui.latex_to_text(acc)
            placeholder.markdown(answer)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Generation failed: {exc}")
            st.session_state.history.pop()  # roll back the unanswered user turn
            return

        with st.expander("Sources", expanded=True):
            st.markdown(ui.format_sources(sources))

        turn = {"role": "assistant", "content": answer, "sources": sources}

        if out_kind == "voice":
            try:
                from src.speech import tts

                with st.spinner("Synthesising speech…"):
                    audio = tts.synthesize(answer)
                mime = tts.audio_mime()
                if audio:
                    turn["audio"] = audio
                    turn["audio_mime"] = mime
                    if will_rerun:
                        # The caller reruns to reset the mic; let _render_history
                        # autoplay this turn on the next run instead of here.
                        st.session_state.pending_autoplay = True
                    else:
                        st.audio(audio, format=mime, autoplay=True)
            except Exception as exc:  # noqa: BLE001
                st.warning(f"Text-to-speech unavailable: {exc}")

        st.session_state.history.append(turn)


def main() -> None:
    st.set_page_config(
        page_title="APICN004 · Income Tax RAG VoiceBot", page_icon="🧾", layout="centered"
    )
    _init_state()

    with st.sidebar:
        st.title("🧾 APICN004")
        st.caption("Indian Income Tax RAG VoiceBot")
        mode = st.radio("Interaction mode", list(ui.MODES.keys()), index=0)
        st.info(ui.MODE_HELP[mode])
        try:
            ret = core.get_retriever()
            st.caption(f"Index: {ret.count:,} chunks")
        except Exception:
            st.caption("Index: not built yet")
        if st.button("Clear conversation"):
            st.session_state.history = []
            st.session_state.last_audio_hash = None
            st.rerun()

    st.markdown("### Ask about Indian Income Tax")
    _render_history()

    in_kind, out_kind = ui.mode_io(mode)
    if _get_retriever_or_warn() is None:
        return

    if in_kind == "text":
        question = st.chat_input("Type your tax question…")
        if question:
            _handle_question(question.strip(), out_kind)
    else:
        audio_val = st.audio_input(
            "🎙️ Record your question, then release to transcribe",
            key=f"audio_{st.session_state.audio_key}",
        )
        if audio_val is not None:
            audio_bytes = audio_val.getvalue()
            digest = hashlib.sha1(audio_bytes).hexdigest()
            if digest != st.session_state.last_audio_hash:
                st.session_state.last_audio_hash = digest
                from src.speech import stt

                with st.spinner("Transcribing…"):
                    try:
                        question = stt.transcribe_bytes(audio_bytes)
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Transcription failed: {exc}")
                        question = None
                if question and question.strip().lower() not in {"quit", "exit", "stop"}:
                    st.success(f"Heard: “{question}”")
                    _handle_question(question.strip(), out_kind, will_rerun=True)
                    # Reset the recorder so the next question can be asked straight away.
                    st.session_state.audio_key += 1
                    st.rerun()
                elif not question:
                    st.warning("Could not transcribe that recording — please try again.")


def _cli() -> None:
    """Command-line entry point: `python src/app.py --mode tito --question "..."`.

    Mirrors the four modes without the Streamlit runtime so the pipeline can be driven
    headlessly (e.g. by an automated evaluator). `--question` answers once and exits;
    omitting it starts an interactive loop. Voice-output modes speak the answer; voice
    input in the CLI falls back to typed input (the browser mic lives in the Streamlit UI).
    """
    import argparse

    from src.speech import tts as _tts

    parser = argparse.ArgumentParser(description="APICN004 — Indian Income Tax RAG VoiceBot")
    parser.add_argument("--mode", choices=["tito", "tivo", "vito", "vivo"], default="tito")
    parser.add_argument("--question", help="one-shot question; omit for an interactive loop")
    args = parser.parse_args()

    _in_kind, out_kind = ui.mode_io(args.mode.upper())
    history: list[dict] = []

    def _answer(question: str) -> None:
        res = core.answer_question(question, history=history)
        answer = ui.latex_to_text(res["answer"])
        print(f"\n{answer}\n")
        print(f"Sources: {core.format_sources(res['sources'])}")
        if core.config.show_timing():
            print(f"Timings: {res['timings']}")
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        if out_kind == "voice":
            try:
                _tts.speak(answer)
            except Exception as exc:  # noqa: BLE001
                print(f"[text-to-speech unavailable: {exc}]")

    if args.question:
        _answer(args.question)
        return

    print(f"APICN004 [{args.mode}] — type a question (empty line or 'quit' to exit).")
    while True:
        try:
            q = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q or q.lower() in {"quit", "exit", "stop"}:
            break
        _answer(q)


def _in_streamlit() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:  # noqa: BLE001
        return False


if __name__ == "__main__":
    if _in_streamlit():
        main()
    else:
        _cli()
