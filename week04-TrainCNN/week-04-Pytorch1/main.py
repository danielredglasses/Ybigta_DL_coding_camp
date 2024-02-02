import argparse
import logging
import os

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam
from torchvision import transforms as T
from tqdm import tqdm

from dataset import FoodDataset
from model import vanillaCNN, vanillaCNN2, VGG19

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    handlers = [logging.StreamHandler()]
)

# Device
if torch.cuda.is_available():
    device = torch.device('cuda')
elif torch.backends.mps.is_available():
    device = torch.device('mps')
else:
    device = torch.device('cpu')

# Parse argument
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, choices=['CNN1', 'CNN2', 'VGG'], required=True, help='model architecture to train')
    parser.add_argument('-e', '--epoch', type=int, default=100, help='the number of train epochs')
    parser.add_argument('-b', '--batch', type=int, default=32, help='batch size')
    parser.add_argument('-lr', '--learning_rate', type=float, default=1e-4, help='learning rate')
    return parser.parse_args()

# Train
def train(model, optimizer, criterion, train_loader):
    model.train()
    train_loss = 0
    correct, total = 0, 0
    for step, data in enumerate(tqdm(train_loader)):
        inputs, targets = data['input'], data['target']
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()

        logger.debug(f'Step {step} loss: {loss}')

        optimizer.step()
        train_loss += loss.item()
        _, predicted = outputs.max(1)

        correct += predicted.eq(targets).sum().item()
        total += targets.shape[0]

    return {
        'train_loss': train_loss,
        'correct': correct,
        'total': total
    }

# Validation
def val(dmodel, criterion, val_loader):
    model.eval()
    val_loss = 0
    correct, total = 0, 0
    with torch.no_grad():
        for _, data in enumerate(tqdm(val_loader)):
            inputs, targets = data['input'], data['target']
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            val_loss += loss.item()
            _, predicted = outputs.max(1)

            correct += predicted.eq(targets).sum().item()
            total += targets.shape[0]
    
    return {
        'val_loss' : val_loss,
        'correct': correct,
        'total': total
    }

if __name__ == '__main__':
    args = parse_args()
    
    os.makedirs('./save', exist_ok=True)
    os.makedirs(f'./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}', exist_ok=True)
    
    transforms = T.Compose([
        T.Resize((227,227), interpolation=T.InterpolationMode.BILINEAR),
        T.RandomVerticalFlip(0.5),
        T.RandomHorizontalFlip(0.5),
    ])

    train_dataset = FoodDataset("./data", "train", transforms=transforms)
    train_loader = DataLoader(train_dataset, batch_size=args.batch, shuffle=True)
    val_dataset = FoodDataset("./data", "val", transforms=transforms)
    val_loader = DataLoader(val_dataset, batch_size=args.batch, shuffle=True)
    
    if args.model == 'CNN1':
        model = vanillaCNN()
    elif args.model == 'CNN2':
        model = vanillaCNN2()
    elif args.model == 'VGG': 
        model = VGG19()
    else:
        raise ValueError("model not supported")
    
    model = model.to(device)
        
    ##########################   fill here   ###########################
        
    # TODO : Training Loop을 작성해주세요
    # 1. logger, optimizer, criterion(loss function)을 정의합니다.
    # train loader는 training에 val loader는 epoch 성능 측정에 사용됩니다.
    # torch.save()를 이용해 epoch마다 model이 저장되도록 해 주세요

    optimizer = Adam(model.parameters(), lr = args.learning_rate)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(1, args.epoch+1):
        # Train model
        logger.info(f'Training Epoch {epoch}')
        train_info = train(model, optimizer, criterion, train_loader)
        train_loss = train_info["train_loss"] / train_info["total"]
        logger.info(f'Epoch {epoch} Loss: {train_loss}')

        # Validate model
        logger.info(f'Validating Epoch {epoch}')
        val_info = val(model, criterion, val_loader)
        val_acc = val_info["correct"] / val_info["total"]
        logger.info(f'Epoch {epoch} accuracy = {val_acc}')

        # Save model
        base_path = f'./save/{args.model}_{args.epoch}_{args.batch}_{args.learning_rate}/'
        file_path = os.path.join(base_path, f'{epoch}_score:{round(val_acc, 3)}.pt')
        torch.save(model, file_path)

    ######################################################################