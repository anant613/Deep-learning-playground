# PyTorch Deep Learning Notes

## 1. Data Preparation
```python
# Linear regression formula: y = weight * X + bias
weight = 0.7
bias = 0.3

# Create data
X = torch.arange(start, end, step).unsqueeze(dim=1)
y = weight * X + bias

# Split data (80/20)
train_split = int(0.8 * len(X))
X_train, y_train = X[:train_split], y[:train_split]
X_test, y_test = X[train_split:], y[train_split:]
```

## 2. Model Creation
```python
# Sequential model
model = nn.Sequential(nn.Linear(1, 1))

# Custom model class
class LinearModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(1, 1)
    
    def forward(self, x):
        return self.linear(x)
```

## 3. Training Components
```python
# Loss function
loss_fn = nn.L1Loss()  # Mean Absolute Error

# Optimizer
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
```

## 4. Training Loop
```python
epochs = 200

for epoch in range(epochs):
    model.train()
    
    # Forward pass
    y_pred = model(X_train)
    loss = loss_fn(y_pred, y_train)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # Print progress
    if epoch % 10 == 0:
        print(f"Epoch: {epoch}, Loss: {loss.item()}")
```

## 5. Evaluation
```python
model.eval()
with torch.inference_mode():
    y_test_pred = model(X_test)
    test_loss = loss_fn(y_test_pred, y_test)
```

## 6. Key Concepts
- **torch.unsqueeze(dim=1)**: Adds dimension for proper tensor shape
- **model.train()**: Sets model to training mode
- **model.eval()**: Sets model to evaluation mode
- **torch.inference_mode()**: Disables gradient computation for faster inference
- **optimizer.zero_grad()**: Clears gradients from previous step
- **loss.backward()**: Computes gradients
- **optimizer.step()**: Updates model parameters

## 7. Common Issues
- **Data splitting bug**: Use `X[train_split:]` not `X[train_split]` for test set
- **Tensor shapes**: Always check input/output dimensions match model expectations
- **Gradient accumulation**: Always call `optimizer.zero_grad()` before backward pass