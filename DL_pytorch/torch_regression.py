import torch
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt

#generate data
x=torch.unsqueeze(torch.linspace(-1,1,100),dim=1)
y=x.pow(2)+0.2*torch.rand(x.size())



# plt.scatter(x.data.numpy(),y.data.numpy())
# plt.show()

#define a net
class Net(torch.nn.Module):
    def __init__(self,n_features,n_hidden,n_output):
        super(Net,self).__init__()#继承，官方写法
        self.hidden=torch.nn.Linear(n_features,n_hidden)#输入个数，输出个数
        self.predict=torch.nn.Linear(n_hidden,n_output)

#真正搭建
    def forward(self, x):#x input
        # x=torch.relu(self.hidden(x))
        x=F.relu(self.hidden(x))
        x=self.predict(x)
        return x

net=Net(n_features=1,n_hidden=10,n_output=1)#1 in 10 ,hidden neural, 1 out
print(net)

#optimzier
# stochastic gradient decent 随机梯度下降,learning rate <1
optmizer=torch.optim.SGD(net.parameters(),lr=0.2)
loss_func=torch.nn.MSELoss()#MSEloss---regression
plt.ion() 

for t in range(100):
    # input x and predict based on x
    prediction=net(x)     
    # must be (1. nn output, 2. target)
    loss=loss_func(prediction,y)
    # clear gradients for next train
    optmizer.zero_grad()
    loss.backward()
    optmizer.step()


    if t % 5 == 0:
    # plot and show learning process
        plt.cla()
        plt.scatter(x.data.numpy(), y.data.numpy())
        plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=5)
        plt.text(0.5, 0, 'Loss=%.4f' % loss.data.numpy(), fontdict={'size': 20, 'color':  'red'})
        plt.pause(0.1)

plt.ioff()
plt.show()