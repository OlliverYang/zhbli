import torch
import torch.nn as nn
import torch.nn.functional as F
import sys
sys.path.append("../")
import gcn3d 

class GCN3D(nn.Module):
    def __init__(self, support_num: int, neighbor_num: int):
        super().__init__()
        self.neighbor_num = neighbor_num
        #pooling_rate = 1
        self.conv_0 = gcn3d.Conv_layer(3,32, support_num= support_num, neighbor_num=neighbor_num)
        self.conv_1 = gcn3d.Conv_layer(32, 64, support_num= support_num, neighbor_num=neighbor_num)
        self.conv_1_2 = gcn3d.Conv_layer(64, 64, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_1_3 = gcn3d.Conv_layer(64, 64, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_1_4 = gcn3d.Conv_layer(64, 64, support_num=support_num, neighbor_num=neighbor_num)
        #self.pool_1 = gcn3d.Pool_layer(pooling_rate=pooling_rate, neighbor_num=pooling_rate)
        self.conv_2 = gcn3d.Conv_layer(64, 128, support_num= support_num, neighbor_num=neighbor_num)
        self.conv_2_2 = gcn3d.Conv_layer(128, 128, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_2_3 = gcn3d.Conv_layer(128, 128, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_2_4 = gcn3d.Conv_layer(128, 128, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_3 = gcn3d.Conv_layer(128, 256, support_num= support_num, neighbor_num=neighbor_num)
        self.conv_3_2 = gcn3d.Conv_layer(256, 256, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_3_3 = gcn3d.Conv_layer(256, 256, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_3_4 = gcn3d.Conv_layer(256, 256, support_num=support_num, neighbor_num=neighbor_num)
        #self.pool_2 = gcn3d.Pool_layer(pooling_rate=pooling_rate, neighbor_num=pooling_rate)
        self.conv_4 = gcn3d.Conv_layer(256, 1024, support_num= support_num, neighbor_num=neighbor_num)
        self.conv_4_2 = gcn3d.Conv_layer(1024, 1024, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_4_3 = gcn3d.Conv_layer(1024, 1024, support_num=support_num, neighbor_num=neighbor_num)
        self.conv_4_4 = gcn3d.Conv_layer(1024, 1024, support_num=support_num, neighbor_num=neighbor_num)

        self.classifier = nn.Sequential(
            nn.Linear(1024, 256), 
            nn.Dropout(0.3),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace= True),
            nn.Linear(256, 2)
        )

    def forward(self,  vertices: "(bs, vertice_num, 3)"):
        bs, vertice_num, _ = vertices.size()
        
        neighbor_index = gcn3d.get_neighbor_index(vertices, self.neighbor_num)
        fm_0 = self.conv_0(neighbor_index=neighbor_index, vertices=vertices, feature_map=vertices)
        fm_1 = self.conv_1(neighbor_index, vertices, fm_0)
        fm_1 = self.conv_1_2(neighbor_index, vertices, fm_1)
        fm_1 = self.conv_1_3(neighbor_index, vertices, fm_1)
        fm_1 = self.conv_1_4(neighbor_index, vertices, fm_1)

        #vertices, fm_1 = self.pool_1(vertices, fm_1)
        #neighbor_index = gcn3d.get_neighbor_index(vertices, self.neighbor_num)

        fm_2 = self.conv_2(neighbor_index, vertices, fm_1)
        fm_2 = self.conv_2_2(neighbor_index, vertices, fm_2)
        fm_2 = self.conv_2_3(neighbor_index, vertices, fm_2)
        fm_2 = self.conv_2_4(neighbor_index, vertices, fm_2)
        fm_3 = self.conv_3(neighbor_index, vertices, fm_2)
        fm_3 = self.conv_3_2(neighbor_index, vertices, fm_3)
        fm_3 = self.conv_3_3(neighbor_index, vertices, fm_3)
        fm_3 = self.conv_3_4(neighbor_index, vertices, fm_3)

        #vertices, fm_3 = self.pool_2(vertices, fm_3)
        #neighbor_index = gcn3d.get_neighbor_index(vertices, self.neighbor_num)
        
        fm_4 = self.conv_4(neighbor_index, vertices, fm_3)
        fm_4 = self.conv_4_2(neighbor_index, vertices, fm_4)
        fm_4 = self.conv_4_3(neighbor_index, vertices, fm_4)
        fm_4 = self.conv_4_4(neighbor_index, vertices, fm_4)
        feature_global = fm_4.max(1)[0]
        pred = self.classifier(feature_global)
        return pred

def test():
    import time
    sys.path.append("..")
    from util import parameter_number
    
    device = torch.device('cuda:0')
    points = torch.zeros(8, 1024, 3).to(device)
    model = GCN3D(support_num= 1, neighbor_num= 20).to(device)
    start = time.time()
    output = model(points)
    
    print("Inference time: {}".format(time.time() - start))
    print("Parameter #: {}".format(parameter_number(model)))
    print("Inputs size: {}".format(points.size()))
    print("Output size: {}".format(output.size()))

if __name__ == '__main__':
    test()