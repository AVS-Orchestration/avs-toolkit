# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml",
# ]
# ///

# ==============================================================================
# Script: assemble_prompt.py
#
# Description:
# This script assembles a complete AVS (Agentic Value Stream) Value Story YAML
# file by combining a YAML-formatted logic file (containing Goal and
# Instructions) with Markdown context files (e.g., job description, raw resume).
# The output is a single, self-contained YAML file that serves as a
# Context-Rich, Algorithmically Legible Prompt for an AI Agent.
#
# Usage:
#   To run this script with `uv` (recommended):
#     uv run assemble_prompt.py [OPTIONS]
#
#   To run this script directly with Python (ensure dependencies are installed):
#     python assemble_prompt.py [OPTIONS]
#
# Options:
#   --logic PATH      Path to the logic (Goal/Instructions) file.
#                     (Default: illustrative-example/VS-001-logic-analysis.md)
#   --job PATH        Path to the Job Description Markdown file.
#                     (Default: illustrative-example/job-description.md)
#   --resume PATH     Path to the Raw Resume Markdown file.
#                     (Default: illustrative-example/raw-resume.md)
#   --output PATH     Path to the output YAML file.
#                     (Default: illustrative-example/VS-001-assembled.yaml)
#
# Example:
#   To run with default files:
#     uv run assemble_prompt.py
#
#   To specify custom input/output files:
#     uv run assemble_prompt.py --job my_job.md --resume my_resume.md --output my_vs.yaml
#
# Dependencies:
#   PyYAML (automatically managed by `uv run` if using `uv`)
# ==============================================================================

import yaml
import os
import argparse

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description="Assemble an AVS Value Story from logic and context files.")
    parser.add_argument("--logic", default="illustrative-example/VS-001-logic-analysis.md", help="Path to the logic (Goal/Instructions) MD/YAML file.")
    parser.add_argument("--job", default="illustrative-example/job-description.md", help="Path to the Job Description MD file.")
    parser.add_argument("--resume", default="illustrative-example/raw-resume.md", help="Path to the Raw Resume MD file.")
    parser.add_argument("--output", default="illustrative-example/VS-001-assembled.yaml", help="Path to the output YAML file.")
    
    args = parser.parse_args()

    print("Assembling Value Story...")

    # 1. Load the Logic (Goal + Instructions)
    print(f"Loading Logic from '{args.logic}'...")
    logic_content = read_file(args.logic)
    logic_data = yaml.safe_load(logic_content)

    # 2. Load the Context (Data)
    print(f"Loading Context from '{args.job}'...")
    job_description = read_file(args.job)

    print(f"Loading Context from '{args.resume}'...")
    raw_resume = read_file(args.resume)

    # 3. Assemble the Value Story
    print("Assembling final structure...")
    value_story = {
        "metadata": {
            "version": "1.0",
            "story_id": "VS-001-assembled",
            "status": "active",
            "generated_by": "assemble_prompt.py"
        },
        # Ingesting the Goal and Instructions directly
        "goal": logic_data['goal'],
        "instructions": logic_data['instructions'],
        
        # Embedding the Context directly (No URIs!)
        "context": {
            "description": "Assembled context from local files.",
            "assets": [
                {
                    "name": "Job Description",
                    "source_file": os.path.basename(args.job),
                    "content": job_description
                },
                {
                    "name": "Raw Candidate Resume",
                    "source_file": os.path.basename(args.resume),
                    "content": raw_resume
                }
            ],
            "implicit_knowledge_overrides": [
                "Assume industry best practices for resume tailoring."
            ]
        },
        "product": {
            "type": "Document",
            "format": "Markdown",
            "handoff_target": "VS-002-resume-generation"
        }
    }

    # 4. Write the Assembled YAML
    with open(args.output, 'w') as f:
        f.write("# ==============================================================================\n")
        f.write("# AUTO-GENERATED VALUE STORY\n")
        f.write("# This file was assembled by 'assemble_prompt.py'\n")
        f.write("# It contains the Goal, Instructions, and FULL CONTEXT needed by the Agent.\n")
        f.write("# ==============================================================================\n\n")
        yaml.dump(value_story, f, sort_keys=False, indent=2, width=80)

    print(f"Successfully assembled '{args.output}'")

if __name__ == "__main__":
    main()
