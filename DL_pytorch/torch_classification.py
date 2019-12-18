import torch
from torch.autograd import Variable
import torch.nn.functional as F
import matplotlib.pyplot as plt

n_data = torch.ones(100, 2)
x0 = torch.normal(2*n_data, 1)      # class0 x data (tensor), shape=(100, 2)
y0 = torch.zeros(100)               # class0 y data (tensor), shape=(100, 1)
x1 = torch.normal(-2*n_data, 1)     # class1 x data (tensor), shape=(100, 2)
y1 = torch.ones(100)                # class1 y data (tensor), shape=(100, 1)
x = torch.cat((x0, x1), 0).type(torch.FloatTensor)  # shape (200, 2) FloatTensor = 32-bit floating
y = torch.cat((y0, y1), ).type(torch.LongTensor)    # shape (200,) LongTensor = 64-bit integer

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

net=Net(n_features=2,n_hidden=10,n_output=2)#2 input, 2 output(2 class)
print(net)

optmizer=torch.optim.SGD(net.parameters(),lr=0.02)
loss_func=torch.nn.CrossEntropyLoss()#classification output probability 
#[0,0,1] label
#[0.1,0.2,0.7] probability
plt.ion() 

for t in range(100):
    # input x and predict based on x
    out=net(x)     
    # must be (1. nn output, 2. target)
    loss=loss_func(out,y)
    # clear gradients for next train
    optmizer.zero_grad()
    loss.backward()
    optmizer.step()

    if t % 2 == 0:
        # plot and show learning process
         plt.cla()
         prediction = torch.max(F.softmax(out), 1)[1]#softmax转换为概率,[1]表示概率最大的index,[0]为最大概率
         pred_y = prediction.data.numpy()
         target_y = y.data.numpy()
         plt.scatter(x.data.numpy()[:, 0], x.data.numpy()[:, 1], c=pred_y, s=100, lw=0, cmap='RdYlGn')
         accuracy = float((pred_y == target_y).astype(int).sum()) / float(target_y.size)
         plt.text(1.5, -4, 'Accuracy=%.2f' % accuracy, fontdict={'size': 20, 'color':  'red'})
         plt.pause(0.1)

plt.ioff()
plt.show()