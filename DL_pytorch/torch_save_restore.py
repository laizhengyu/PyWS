import torch

import matplotlib.pyplot as plt

#generate data
x=torch.unsqueeze(torch.linspace(-1,1,100),dim=1)
y=x.pow(2)+0.2*torch.rand(x.size())
# plt.scatter(x.data.numpy(),y.data.numpy())
# plt.show()




def save():
    net1=torch.nn.Sequential(
    torch.nn.Linear(1,10),
    torch.nn.ReLU(),
    torch.nn.Linear(10,1),
    )


    #optimzier
    # stochastic gradient decent 随机梯度下降,learning rate <1
    optmizer=torch.optim.SGD(net1.parameters(),lr=0.2)
    loss_func=torch.nn.MSELoss()#MSEloss---regression
    

    for t in range(100):
    # input x and predict based on x
      prediction=net1(x)     
    # must be (1. nn output, 2. target)
      loss=loss_func(prediction,y)
    # clear gradients for next train
      optmizer.zero_grad()
      loss.backward()
      optmizer.step()
    
    # plot result
    plt.figure(1, figsize=(10, 3))
    plt.subplot(131)
    plt.title('Net1')
    plt.scatter(x.data.numpy(), y.data.numpy())
    plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=5)

    #2 method to save
    torch.save(net1,'net.pkl')#entire net
    torch.save(net1.state_dict(),'net_parameter.pkl')#only parameter

def restore_net():
    net2=torch.load('net.pkl')
    prediction=net2(x)

    plt.subplot(132)
    plt.title('Net2')
    plt.scatter(x.data.numpy(), y.data.numpy())
    plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=5)

def restore_net_parameter():
    net3=torch.nn.Sequential(
    torch.nn.Linear(1,10),
    torch.nn.ReLU(),
    torch.nn.Linear(10,1),
    )
    net3.load_state_dict(torch.load('net_parameter.pkl'))
    prediction = net3(x)

    # plot result
    plt.subplot(133)
    plt.title('Net3')
    plt.scatter(x.data.numpy(), y.data.numpy())
    plt.plot(x.data.numpy(), prediction.data.numpy(), 'r-', lw=5)
    plt.show()

save()
restore_net()
restore_net_parameter()
