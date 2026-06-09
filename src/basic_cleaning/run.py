#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    logger.info("cleaning data")
    run.config.update(args)

    artifact_dir = run.use_artifact(args.input_artifact).download()
    local_path = os.path.join(artifact_dir, "sample1.csv")
    df = pd.read_csv(local_path)

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    df.to_csv("clean_sample.csv", index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="name of the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="W&B output type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="output description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
