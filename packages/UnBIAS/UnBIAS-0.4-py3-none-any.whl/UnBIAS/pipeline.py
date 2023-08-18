from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTokenClassification, AutoModelForSeq2SeqLM

def combined_pipeline(text):
    # Classification
    classifier_tokenizer = AutoTokenizer.from_pretrained("newsmediabias/UnBIAS-classifier")
    classifier_model = AutoModelForSequenceClassification.from_pretrained("newsmediabias/UnBIAS-classifier")
    classifier = pipeline("text-classification", model=classifier_model, tokenizer=classifier_tokenizer)
    classification_result = classifier(text)

    # Named Entity Recognition
    ner_tokenizer = AutoTokenizer.from_pretrained("newsmediabias/UnBIAS-Named-entity")
    ner_model = AutoModelForTokenClassification.from_pretrained("newsmediabias/UnBIAS-Named-entity")
    ner = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)
    ner_result = ner(text)

    # Debiasing
    debiaser_tokenizer = AutoTokenizer.from_pretrained("newsmediabias/UnBIAS-Debiaser")
    debiaser_model = AutoModelForSeq2SeqLM.from_pretrained("newsmediabias/UnBIAS-Debiaser")
    inputs = debiaser_tokenizer(text, return_tensors="pt", truncation=True, padding='max_length', max_length=512)
    output = debiaser_model.generate(inputs['input_ids'], attention_mask=inputs['attention_mask'], max_length=100)
    debiaser_result = debiaser_tokenizer.decode(output[0], skip_special_tokens=True)

    return {
        "classification": classification_result,
        "ner": ner_result,
        "debiasing": debiaser_result
    }