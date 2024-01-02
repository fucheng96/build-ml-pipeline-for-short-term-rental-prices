#!/usr/bin/env python
"""
Splits data into train and test datasets and save the results in Weights & Biases
"""
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="data_split")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This step splits data into train & test")


    parser.add_argument(
        "--test_size", 
        type=## INSERT TYPE HERE: str, float or int,
        help=## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--stratify_by", 
        type=## INSERT TYPE HERE: str, float or int,
        help=## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--random_seed", 
        type=## INSERT TYPE HERE: str, float or int,
        help=## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
