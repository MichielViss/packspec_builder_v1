# <ins> Packspec Builder </ins>
Code to build a packspec builder from material master

### Consider defining the solution according to bin types
Bin types are used to define the operational limits for a storage bin. Namely the maximum operating weight, volume, length, width and height. Bin types can help us determine where a product should live
Consider currently what bin types exist in what storage type
Use storage bin type dimension data to determine what the optimal packaging size should be

### Configured bin types
| Storage Bin Type | Bin Access Type |
|---|---|
|Y13A | 1.3 Meter High Pallet Bin - All Weight|
|Y18H | 1.8 Meter High Pallet - Heavy Weight Bin|
|Y18L | 1.8 Meter High Pallet - Light Weight Bin|
|Y18D | 1.8 Meter High Pallet - Double Bin |
|YHPL | Half Pallet Bin - All Weights|

### Bin type, volume and weight table

| Storage Bin Type | Bin Access Type | Maximum Weight | Weight Unit | Maximum Volume | Volume Unit |
|---|---|---|---|---|---|
|Y13A | MUP2 | 1,000 | KG | 1,560 | CD3|
|Y13A | MUP6 | 1,000 | KG | 1,560 | CD3|
|Y13A | MUP9 | 1,000 | KG | 1,560 | CD3|
|Y18H | HAND | 1,000 | KG | 2,500 | CD3|
|Y18L | MUP9 | 300 | KG | 2,500 | CD3|
|YHPL | HAND | 1,000 | KG | 780 | CD3|
|Y18D | MUP6 | 2,000 | KG | 3,120 | CD3|
|Y18D | MUP2 | 2,000 | KG | 3,120 | CD3|
|Y18D | MUP9 | 2,000 | KG | 3,120 | CD3|
|Y13A | HAND | 1,000 | KG | 1,560 | CD3|
|YHPL | MUP2 | 1,000 | KG | 780 | CD3|
|YHPL | MUP6 | 1,000 | KG | 780 | CD3|
|YHPL | MUP9 | 1,000 | KG | 780 | CD3|

Current logic used in definig the bin type to storage bin allocation
+ Floor bins are in R021 storage type R122 storage section with bin type Y18H (1000 kg, 2500 cd3) 
