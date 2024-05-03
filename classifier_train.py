import argparse
import yaml
from trainers import CustomClassifierTrainer
from dataset import ClassifierDataset, ClassifierDataCollator
from transformers import BertForSequenceClassification, BertTokenizer, BertConfig


def load_config_from_yaml(config_file):
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


def main(config):

    bert_config = BertConfig.from_pretrained(config["model_name"])
    bert_config.num_labels = config["num_labels"]
    bert_config.problem_type = "single_label_classification"
    tokenizer = BertTokenizer.from_pretrained(config["model_name"])
    model = BertForSequenceClassification.from_pretrained(
        config["model_name"], config=bert_config
    )

    train_dataset = ClassifierDataset(
        data_path=config["train_file"],
        lang=config["language"],
    )

    eval_dataset = ClassifierDataset(
        data_path=config["eval_file"],
        lang=config["language"],
    )

    data_collator = ClassifierDataCollator(
        tokenizer=tokenizer, max_length=config["max_seq_length"]
    )
    # Initialize Trainer with configurations from the YAML file
    trainer = CustomClassifierTrainer(
        model=model,
        train_dataset=train_dataset,
        val_dataset=eval_dataset,
        batch_size=config["batch_size"],
        lr=config["lr"],
        max_grad_norm=config["max_grad_norm"],
        device=config["device"],
        distributed=config["distributed"],
        patience=config["patience"],
        log_dir=config["log_dir"],
        data_collator=data_collator,
    )
    trainer.train(config["epochs"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Training script")
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to YAML configuration file",
    )
    args = parser.parse_args()

    config = load_config_from_yaml(args.config)
    main(config)
