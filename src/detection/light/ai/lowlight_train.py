import torch
import torch.optim
import os
import argparse
import dataloader
import model
import Myloss


def weights_init(m):
    """
    Initializes the weights of a given model layer.

    Args:
        m (torch.nn.Module): Model layer that requires weight initialization.
    """
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


def train(config):
    """
    Trains the EnhanceNet model on a low-light dataset.
    
    Args:
        config (argparse.Namespace): Configuration object containing training parameters.
            - `lowlight_images_path` (str): Path to the low-light image dataset.
            - `lr` (float): Learning rate.
            - `weight_decay` (float): Weight decay for the optimizer.
            - `grad_clip_norm` (float): Gradient clipping norm.
            - `num_epochs` (int): Number of epochs to train.
            - `train_batch_size` (int): Training batch size.
            - `num_workers` (int): Number of workers for loading data.
            - `display_iter` (int): Number of iterations after which to display the loss.
            - `snapshot_iter` (int): Number of iterations after which to save model snapshots.
            - `snapshots_folder` (str): Folder to save model snapshots.
            - `load_pretrain` (bool): Whether to load pre-trained weights.
            - `pretrain_dir` (str): Path to pre-trained weights.
    """
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

    # Initialize model
    DCE_net = model.enhance_net_nopool().cuda()

    DCE_net.apply(weights_init)
    if config.load_pretrain:
        DCE_net.load_state_dict(torch.load(config.pretrain_dir))
    # Load dataset
    train_dataset = dataloader.lowlight_loader(config.lowlight_images_path)

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=config.train_batch_size, shuffle=True,
                                               num_workers=config.num_workers, pin_memory=True)

    # Define loss functions
    L_color = Myloss.L_color()
    L_spa = Myloss.L_spa()

    L_exp = Myloss.L_exp(16, 0.6)
    L_TV = Myloss.L_TV()

    # Define optimizer
    optimizer = torch.optim.Adam(DCE_net.parameters(), lr=config.lr, weight_decay=config.weight_decay)

    DCE_net.train()

    # Training loop
    for epoch in range(config.num_epochs):
        for iteration, img_lowlight in enumerate(train_loader):

            img_lowlight = img_lowlight.cuda()

            # Forward pass
            enhanced_image_1, enhanced_image, A = DCE_net(img_lowlight)

            # Compute losses
            Loss_TV = 200 * L_TV(A)

            loss_spa = torch.mean(L_spa(enhanced_image, img_lowlight))

            loss_col = 5 * torch.mean(L_color(enhanced_image))

            loss_exp = 10 * torch.mean(L_exp(enhanced_image))

            # best_loss
            loss = Loss_TV + loss_spa + loss_col + loss_exp
            #

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm(DCE_net.parameters(), config.grad_clip_norm)
            optimizer.step()
            # Display training progress
            if ((iteration + 1) % config.display_iter) == 0:
                print("Loss at iteration", iteration + 1, ":", loss.item())
            # Save model snapshots
            if ((iteration + 1) % config.snapshot_iter) == 0:
                torch.save(DCE_net.state_dict(), config.snapshots_folder + "Epoch" + str(epoch) + '.pth')


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()

    # Input Parameters
    parser.add_argument('--lowlight_images_path', type=str, default="C:/Users/salah/Zero-DCE_code/data/train_data/")
    parser.add_argument('--lr', type=float, default=0.0001)
    parser.add_argument('--weight_decay', type=float, default=0.0001)
    parser.add_argument('--grad_clip_norm', type=float, default=0.1)
    parser.add_argument('--num_epochs', type=int, default=200)
    parser.add_argument('--train_batch_size', type=int, default=8)
    parser.add_argument('--val_batch_size', type=int, default=4)
    parser.add_argument('--num_workers', type=int, default=4)
    parser.add_argument('--display_iter', type=int, default=10)
    parser.add_argument('--snapshot_iter', type=int, default=10)
    parser.add_argument('--snapshots_folder', type=str, default="snapshots/")
    parser.add_argument('--load_pretrain', type=bool, default=False)
    parser.add_argument('--pretrain_dir', type=str, default="snapshots/Epoch99.pth")

    config = parser.parse_args()

    if not os.path.exists(config.snapshots_folder):
        os.mkdir(config.snapshots_folder)

    train(config)
