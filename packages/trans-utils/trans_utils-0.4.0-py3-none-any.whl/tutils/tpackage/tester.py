

class Tester(object):
    def __init__(self, logger=None, config=None, args=None, mode='subtest'):

        dataset_1 = Test_Cephalometric(config['dataset']['pth'], mode=mode)
        self.dataloader = DataLoader(dataset_1, batch_size=1,
                                       shuffle=False, num_workers=2)
        # self.Radius = dataset_1.Radius
        self.config = config
        self.evaluater = Evaluater(logger, [384, 384],
                                       [2400, 1935])
        self.logger = logger

        self.dataset = dataset_1
        self.id_landmarks = [i for i in range(config['special']['num_landmarks'])]

    def test(self, model, epoch=0, rank=-1):
        self.evaluater.reset()
        model.eval()
        ID = 1
        for data in tqdm(self.dataloader, ncols=100):
            if rank >= 0:
                img = data['img'].to(rank)
            else:
                img = data['img'].cuda()
            landmark_list = data['landmark_list']
            heatmap = model(img)
            pred_landmark = heatmap2landmark(heatmap.cpu().detach().numpy()[0])

            # pred_landmark = np.unravel_index(heatmap.argmax(), heatmap.shape)

            self.evaluater.record(pred_landmark, landmark_list)

            # Optional Save viusal results
            # image_pred = visualize(img, pred_landmark, landmark_list)
            # image_pred.save(os.path.join('visuals', str(ID) + '_pred.png'))

            ID += 1

        return self.evaluater.cal_metrics_all()