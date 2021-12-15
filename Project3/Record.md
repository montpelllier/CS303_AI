# Record

12-15 22:20

优化器采用Adam，在YourNet类中采用量化QuantStub和DeQuantStub。

结果：

| Model Name | Accuracy | Infer Time(ms) | Params(M) | MACs(M) |
| ---------- | -------- | -------------- | --------- | ------- |
| YourNet    | 0.977    | 0.234          | 0.206     | 0.060   |



