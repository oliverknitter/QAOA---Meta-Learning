import argparse
import numpy as np

def str2bool(v):
    return v.lower() in ('true', '1')

arg_lists = []
parser = argparse.ArgumentParser()

def add_argument_group(name):
    arg = parser.add_argument_group(name)
    arg_lists.append(arg)
    return arg

def define_args_parser():
    parser = argparse.ArgumentParser(description='Benchmark settings.')
    return parser

# Network
net_arg = add_argument_group('Network')
net_arg.add_argument('--learning_rate', '-l', default=0.05, type=float, help='The learning rate')
net_arg.add_argument('--kernel_size', '-k', type=int, default=4, help='The kernel size of each conv layer')
net_arg.add_argument('--depth', '-d', type=int, default=1, help='Num of layers before sum pooling')
net_arg.add_argument('--width', '-w', type=int, default=1, help='Num of output channels in each layer')
net_arg.add_argument('--activation', type=str, choices=["relu", "tanh"], default="tanh", help='The activation function')
net_arg.add_argument('--model_name', '-m', type=str, \
                     choices=["rbm","rbm_real","mlp","conv_net"], \
                     default='rbm', help='Model architecture')
net_arg.add_argument('--param_init', type=float, default=0.01, help='Model parameter initialization')

# Data
data_arg = add_argument_group('Data')
data_arg.add_argument('--pb_type', type=str, choices=["maxcut", "spinglass", "spinglass-SK"], default="maxcut", help='The problem type')
data_arg.add_argument('--batch_size', '-b', type=int, default=128, help='The batch size in each iteration')
data_arg.add_argument('--input_size', '-i', nargs="+", type=int, default=(20,1), help='Number of spins in the input')
data_arg.add_argument('--num_of_iterations', '-ni', type=int, default=0, help='Num of iterations to benchmark')

# Train
train_arg = add_argument_group('Training')
train_arg.add_argument('--epochs', type=int, default=200)
train_arg.add_argument('--use_cholesky', type=str2bool, default=True, help='use cholesky solver in SR')
train_arg.add_argument('--use_iterative', type=str2bool, default=True, help='use iterative solver in SR')
train_arg.add_argument('--optimizer', \
                       choices=["adadelta","adagrad","adamax","momentum","rmsprop","sgd"], \
                       default="sgd", help='The optimizer for training')
train_arg.add_argument('--use_sr', type=str2bool, default=True, help='use stochastic reconfiguration for training')
train_arg.add_argument('--decay_factor', type=float, default=1.0, help='Training decay factor')

# Misc
misc_arg = add_argument_group('Misc')
misc_arg.add_argument('--framework', '-fr', type=str, \
                      choices= ["netket","random_cut","greedy_cut","goemans_williamson","manopt", "reptile_demo"], \
                      default='netket', help='Options for algorithms')
misc_arg.add_argument('--dir', type=str, default='')
misc_arg.add_argument('--num_gpu', type=int, default=0)
misc_arg.add_argument('--num_trials', type=int, default=1, help='Number of runs with different seeds; also serves as number of metatrain iterations')
misc_arg.add_argument('--random_seed', '-r', type=int, default=600, help='Randomization seed')
misc_arg.add_argument('--present', type=str, default="boxplot")

misc_arg.add_argument('--random_example', '-rex', type=str2bool, default=False, help='Program generates a random example instead of running a specific one.')
misc_arg.add_argument('--transverse', type=float, default=0.0, help='Currently applies a uniform transverse field component to the Hamiltonian')

# Meta-learning
meta_arg = add_argument_group('Metalearning')
meta_arg.add_argument('--metalearner', '-ml', type=str, choices=['reptile', 'iMAML'], default='reptile', help='Choice of algorithm for meta-learning')
meta_arg.add_argument('--metalearning_rate', '-mlr', default=0.05, type=float, help='The meta-learning rate')
meta_arg.add_argument('--metabatch_size', '-mb', type=int, default=1, help='The batch size used for each meta-training update.')
meta_arg.add_argument('--metatrain', type=str2bool, default=False, help='Program performs meta-learning training on --num_trials examples with --num_of_iterations inner loops.')
meta_arg.add_argument('--metatest', type=str2bool, default=False, help='Program uses initialization from previous metatraining.')


def get_config():
    cf, unparsed = parser.parse_known_args()
    if len(cf.input_size) == 1:
        cf.input_size = (cf.input_size[0],)
    elif len(cf.input_size) == 2:
        cf.input_size = (cf.input_size[0],cf.input_size[1])
    else:
        raise("input dimension must be either 1 or 2")
    if cf.num_of_iterations == 0:
        cf.num_of_iterations = int(50 + 10*cf.batch_size/1024)
    return cf, unparsed
