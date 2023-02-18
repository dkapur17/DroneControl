model1 => Trained on [dxt, dyt, dxo, dyo, vx, vy] (Here vx, vy are the drone's physical velocity). The environment still had a frontwall penalty, but was removed during evaluation and the agent performed well.

model2 => Back to basics [dxt, dyt, dxo, dyo]. Added front wall penalty, and got back old reward function.