import os
from dotenv import load_dotenv
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from datasets import load_dataset, Dataset

class WyrModelTrainer:
    def __init__(self, model_name: str = 'gpt2'):
        """
        Initializes the model trainer with a pre-trained model and tokenizer.
        """
        load_dotenv()
        self.output_path = os.environ.get("OUTPUT_DIR")
        if not self.output_path:
            raise ValueError("OUTPUT_DIR environment variable is not set.")

        self.model_name = model_name
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = GPT2LMHeadModel.from_pretrained(model_name)

    def _prepare_data(self):
        # Load your datasets where each entry is a full question
        train_dataset = load_dataset('json', data_files=os.path.join(self.output_path, 'train_data.json'),
                                     split='train')
        val_dataset = load_dataset('json', data_files=os.path.join(self.output_path, 'val_data.json'), split='train')

        def tokenize_function(examples):
            tokenized_inputs = self.tokenizer(
                examples["text"],
                padding="max_length",
                truncation=True,
                max_length=128
            )
            tokenized_inputs["labels"] = tokenized_inputs["input_ids"]
            return tokenized_inputs

        self.tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
        self.tokenized_val_dataset = val_dataset.map(tokenize_function, batched=True)

    def train(self):
        """
        Starts the fine-tuning process.
        """
        print("Preparing data...")
        self._prepare_data()

        training_args = TrainingArguments(
            output_dir='./wyr_results',
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir='./wyr_logs',
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.tokenized_train_dataset,
            eval_dataset=self.tokenized_val_dataset,
        )

        print("Starting training...")
        trainer.train()
        print("Training complete.")

    def generate_text(self, prompt: str, max_length: int = 128) -> str:
        if not self.model:
            raise RuntimeError("Model has not been trained yet. Call .train() first.")

        device = self.model.device

        # Tokenize the prompt
        inputs = self.tokenizer(prompt, return_tensors='pt')

        # Move inputs to the correct device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        outputs = self.model.generate(
            **inputs,  # Pass the entire inputs dictionary
            max_length=max_length,
            num_return_sequences=1,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text.strip()