feature_and_cls_attack_trainer.py

```python
trainer.train_step(...)	
```

trainer.py

```python
class BRFasterRcnnTrainer:
    def __init__(attacker):
        self.attacker = attacker
    def train_step(...):
        BR_losses = self.attacker.forward(...)
```

attacks.py

```python
class Blade_runner:
    def forward(...):
        for i in range(1):
	        loss_D = (loss_D_fake + loss_D_real) * 0.5
        while loss_feature > 1 and loss_perturb > 1:
            
```

