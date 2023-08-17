from os.path import join
from pathlib import Path
from proquo.model.linking.LinkingModelTrainer import LinkingModelTrainer
from datetime import datetime
from proquo.model.linking.LinkingVectorizer import LinkingVectorizer


def train(train_file_path, val_file_path, output_path):

    x_train = []
    y_train = []

    with open(train_file_path, 'r', encoding='utf-8') as train_file:
        for line in train_file:

            if not line.strip():
                continue

            parts = line.split('\t')

            if len(parts) == 3 or len(parts) == 6:
                x_train.append((parts[0], parts[1]))
                y_train.append(int(parts[2]))
            else:
                print(f'wrong count: {line}')

    x_val = []
    y_val = []

    with open(val_file_path, 'r', encoding='utf-8') as val_file:
        for line in val_file:

            if not line.strip():
                continue

            parts = line.split('\t')

            if len(parts) == 3 or len(parts) == 6:
                x_val.append((parts[0], parts[1]))
                y_val.append(int(parts[2]))
            else:
                print(f'wrong count: {line}')

    now = datetime.now()
    date_time_string = now.strftime("%Y_%m_%d_%H_%M_%S")
    output_date_dir = join(output_path, date_time_string)
    Path(output_date_dir).mkdir(parents=True, exist_ok=True)

    linking_vectorizer = LinkingVectorizer.from_raw(512, True)

    tokenizer_dir = join(output_date_dir, 'tokenizer')
    Path(tokenizer_dir).mkdir(parents=True, exist_ok=True)
    linking_vectorizer.tokenizer.save_pretrained(tokenizer_dir)

    model = LinkingModelTrainer(linking_vectorizer, 4, 3)
    model.train_model(x_train, y_train, x_val, y_val, output_date_dir)
