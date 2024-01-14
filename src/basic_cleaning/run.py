#!/usr/bin/env python
"""
Performs basic data cleaning and save the results in Weights & Biases
"""
# Imort libraries
import argparse
import logging
import pandas as pd
import wandb


# Logging configurations
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)-15s %(message)s"
)
logger = logging.getLogger()


def go(args):
    """
    Performs basic data cleaning and save the results in Weights & Biases
    """
    # Initiate run
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact
    input_artifact_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(input_artifact_path)
    logger.info("basic_cleaning: input_artifact downloaded")

    # Drop price outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    logger.info("basic_cleaning: Price outliers dropped")

    # Drop latitude & longitude outliers
    idx = (
        df['longitude'].between(-74.25, -73.50)
        & df['latitude'].between(40.5, 41.2)
    ) 
    df = df[idx].copy()
    logger.info("basic_cleaning: Latitude & longitude outliers dropped")

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    logger.info("basic_cleaning: Converted last_review to datetime")

    # Save the cleaned dataset
    file_name = args.output_artifact
    df.to_csv(file_name, index=False)
    logger.info("basic_cleaning: output_artifact saved")

    # Add saved artifact to wandb
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(file_name)

    # Log artifact to wandb
    run.log_artifact(artifact)
    logger.info("basic_cleaning: Artifact logged")


if __name__ == "__main__":
    # Instantiate parser
    parser = argparse.ArgumentParser(
        description="This step preprocesses the data"
    )

    # Add arguments into parser
    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the input_artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of output_artifact to be created and saved in wandb",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output_artifact to create",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of output_artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum rental price in data validation",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum rental price in data validation",
        required=True
    )

    args = parser.parse_args()

    # Run go function with arguments in parser
    go(args)
