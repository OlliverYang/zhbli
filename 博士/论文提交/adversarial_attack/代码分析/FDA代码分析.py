    def get_fda_loss(self, opt_operations):
        loss = 0
        for layer in opt_operations:  # 每个层都要计算损失。
            layer = layer[0]
            batch_size = int(int(layer.shape[0]) / 2)  # batch 为 2，前一半是干净输入，后一半是对抗输入
            tensor = layer[:batch_size]  # 干净张量, shape=[1,w,h,c]
            mean_tensor = tf.stack(
                [tf.reduce_mean(tensor, -1), ] * tensor.shape[-1], -1)  # [1,w,h,c]
			# tf.reduce_mean(tensor, -1).shape = [1,h,w] 沿着通道方向求平均。后复制成原始张量的尺寸。
            wts_good = tensor < mean_tensor  # [1,w,h,c] bool。为1处表示激活大的位置，即支持预测的位置。
            wts_good = tf.to_float(wts_good)
            wts_bad = tensor >= mean_tensor
            wts_bad = tf.to_float(wts_bad)
            loss += tf.log(tf.nn.l2_loss(
                wts_good * (layer[batch_size:]) / tf.cast(tf.size(layer),
                                                          tf.float32)))
            # layer[batch_size:] 是对抗张量
            # 含义是希望支持激活的位置的值尽量小。要除以该层总的激活的数量。
            loss -= tf.log(tf.nn.l2_loss(
                wts_bad * (layer[batch_size:]) / tf.cast(tf.size(layer),
                                                         tf.float32)))
        loss = loss / len(opt_operations)
        return loss

# 说明：对所有的relu层执行此操作。