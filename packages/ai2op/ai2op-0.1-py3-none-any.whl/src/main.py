import os
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from processing import DataProcessor
from finetuning import finetune_model

def main():
    # Get the directory of the currently executing script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        # Instantiate the tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained("Salesforce/xgen-7b-8k-base", trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained("Salesforce/xgen-7b-8k-base", torch_dtype=torch.bfloat16)

        # Set up fine-tuning parameters
        num_epochs = 10
        batch_size = 16
        learning_rate = 1e-5

        # Construct the project directory path using the script's directory
        project_dir = os.path.dirname(script_dir)
        data_dir = os.path.join(project_dir, "training_data")

        print("Instantiating DataProcessor...")
        data_processor = DataProcessor(data_dir)

        print("Processing data...")
        trained_dataset = data_processor.process_data()  # Only train dataset for fine-tuning
        
        if trained_dataset is not None:
            # Calculate validation dataset (val_dataset) for fine-tuning
            val_dataset = trained_dataset.sample(frac=0.2, random_state=42)
            trained_dataset.to_csv(os.path.join(data_dir, "trained_dataset.csv"), index=False)
        else:
            logging.error("Data processing failed.")
            return

        # Fine-tune the model using the imported function
        print("Fine-tuning model...")
        finetune_model(model, trained_dataset, val_dataset, num_epochs, batch_size, learning_rate)

        logging.info("Fine-tuning completed successfully.")

        # Example usage for aipipeline, summarizer, and interpreter
        from transformers import pipeline, TextGenerationPipeline

        # Create an AI pipeline
        aipipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

        # Summarizer
        summarizer = TextGenerationPipeline(model=model, tokenizer=tokenizer)

        # Interpreter
        def interpret(text):
            inputs = tokenizer(text, return_tensors="pt")
            outputs = model(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=-1).item()
            return predicted_class
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

if __name__ == "__main__":
    main()