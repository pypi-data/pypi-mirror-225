import time
import pytz
from datetime import datetime
from typing import Any, Dict, List, Union

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.messages import BaseMessage
from langchain.schema.output import LLMResult

from llm_monitor.schema.transaction import TransactionRecord
from llm_monitor.utils.aggregator import add_record_to_batch, initialize_api_client


class MonitorHandler(BaseCallbackHandler):
    timers = {}
    records = {}

    def __init__(self, project_name: str, *args, **kwargs) -> None:
        initialize_api_client(project_name=project_name)
        super().__init__(*args, **kwargs)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        input_text = prompts[0]
        run_id = kwargs["run_id"]
        self.timers[run_id] = {}
        self.timers[run_id]["start"] = time.perf_counter()

        model = kwargs["invocation_params"]["model_name"]
        self.records[run_id] = TransactionRecord(
            input_text=input_text,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
        )

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        **kwargs: Any,
    ) -> Any:
        """Run when Chat Model starts running."""
        input_text = messages[0][0].content
        run_id = kwargs["run_id"]
        self.timers[run_id] = {}
        self.timers[run_id]["start"] = time.perf_counter()

        model = kwargs["invocation_params"]["model_name"]
        self.records[run_id] = TransactionRecord(
            input_text=input_text,
            model=model,
            created_at=datetime.now(tz=pytz.utc).isoformat(),
        )

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        run_id = kwargs["run_id"]
        self.timers[run_id]["stop"] = time.perf_counter()
        latency_ms = round(
            (self.timers[run_id]["stop"] - self.timers[run_id]["start"]) * 1000
        )
        del self.timers[run_id]

        generation = response.generations[0][0]
        if hasattr(generation, "message"):
            output_text = generation.message.content
        else:
            output_text = generation.text
        usage = response.llm_output["token_usage"]
        num_input_tokens = usage.get("prompt_tokens")
        num_output_tokens = usage.get("completion_tokens")

        self.records[run_id].__dict__.update(
            output_text=output_text,
            num_input_tokens=num_input_tokens,
            num_output_tokens=num_output_tokens,
            latency_ms=latency_ms,
            status_code=200,
        )

        add_record_to_batch(self.records[run_id])
        del self.records[run_id]

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        run_id = kwargs["run_id"]
        self.timers[run_id]["stop"] = time.perf_counter()
        latency_ms = round(
            (self.timers[run_id]["stop"] - self.timers[run_id]["start"]) * 1000
        )
        del self.timers[run_id]

        self.records[run_id].__dict__.update(
            output_text=f"ERROR: {error}",
            num_input_tokens=0,
            num_output_tokens=0,
            latency_ms=latency_ms,
            status_code=error.http_status,
        )

        add_record_to_batch(self.records[run_id])
        del self.records[run_id]
