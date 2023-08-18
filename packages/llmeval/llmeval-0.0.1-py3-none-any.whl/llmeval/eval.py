# Copyright Log10, Inc 2023


from omegaconf import DictConfig, open_dict, OmegaConf

import hydra
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from pprint import pprint
import yaml
import os
import logging

# TODO: Define data class for prompt
# TODO: Define data class for tests


@hydra.main(version_base=None, config_path=".", config_name="llmeval")
def main(cfg: DictConfig) -> None:
    # TODO: Support non-openai models.
    llm = ChatOpenAI()

    for i in range(cfg.n_tries):
        # TODO: If messages is available, assume it is a chat model.
        # TODO: Gather output into report. (Figure out how to run a post-processing step with multi run)

        messages = [(message.role, message.content) for message in cfg.prompts.messages]
        template = ChatPromptTemplate.from_messages(messages)

        metrics = cfg.prompts.tests.metrics
        variables = cfg.prompts.variables

        logging.debug(metrics)

        # Substitute variables in template with reference values.
        for reference in cfg.prompts.tests.references:
            # Verify refernce has all expected variables.
            skip = False
            for variable in variables:
                if variable.name not in reference.input:
                    logging.warn(
                        f"Variable {variable} is not in reference input. Skipping."
                    )
                    skip = True
            if skip:
                continue

            logging.debug(f"reference={reference}")
            messages = template.format_messages(**reference.input)
            logging.debug(f"messages={messages}")
            response = llm(messages)

            with open_dict(reference):
                reference["actual"] = response.content

                for metric_spec in metrics:
                    logging.debug(f"metric={metric_spec}")
                    locals = {"prompt": str(messages), "actual": response.content}

                    if hasattr(reference, "expected"):
                        locals["expected"] = reference.expected

                    exec(metric_spec.code, None, locals)
                    metric_value = locals["metric"]
                    result = locals["result"]
                    logging.debug(f"result={result}")

                    logging.debug(f"metric.name={metric_spec.name}")
                    # Check whether value is already set.
                    if "metrics" not in reference:
                        reference["metrics"] = {}

                    reference["metrics"][metric_spec.name] = {
                        "metric": metric_value,
                        "result": "pass" if result else "fail",
                    }

        with open(f"report-{i}.yaml", "w") as f:
            f.write(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    main()
