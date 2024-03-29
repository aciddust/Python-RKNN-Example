from rknn.api import RKNN

def common_transfer(pb_name,export_name):
        # 특정 로그를 참조하기위함.
        ret = 0
        rknn = RKNN()
        # 이 단계는 grayscale 이미지를 다룰 때 필요하지 않음.
        # rknn.config(channel_mean_value='', reorder_channel='')
        print('--> Loading model')

        ret = rknn.load_tensorflow(
                tf_pb='./mnist_frozen_graph.pb',
                inputs=['x'],
                outputs=['y_conv'],
                input_size_list=[[28,28,1]])
        if ret != 0:
                print('load_tensorflow error')
                rknn.release()
                return ret
        print('done')
        print('--> Building model')
        rknn.build(do_quantization=False)
        print('done')
        # rknn 모델 파일 저장 내보내기
        rknn.export_rknn('./mnist.rknn')
        # Release RKNN Context
        rknn.release()
        return ret

def quantify_transfer(pb_name,dataset_name,export_name):
        ret = 0
        print(pb_name,dataset_name,export_name)
        rknn = RKNN()
        rknn.config(channel_mean_value='', reorder_channel='',quantized_dtype='dynamic_fixed_point-8')
        print('--> Loading model')
        ret = rknn.load_tensorflow(
                tf_pb=pb_name,
                inputs=['x'],
                outputs=['y_conv'],
                input_size_list=[[28,28,1]])
        if ret != 0:
                print('load_tensorflow error')
                rknn.release()
                return ret
        print('done')
        print('--> Building model')
        rknn.build(do_quantization=True,dataset=dataset_name)
        print('done')
        # rknn 모델 파일 저장 내보내기
        rknn.export_rknn(export_name)
        # Release RKNN Context
        rknn.release()
        return ret
if __name__ == '__main__':
        #pb에서 rknn 모델
        pb_name = './mnist_frozen_graph.pb'
        export_name = './mnist.rknn'
        ret = common_transfer(pb_name,export_name)
        if ret != 0:
                print('======common transfer error !!===========')
        else:
                print('======common transfer ok !!===========')
        dataset_name = './dataset.txt'
        export_name = './mnist_quantization.rknn'
        #정량화 된 rknn 모델로 pb
        quantify_transfer(pb_name,dataset_name,export_name)
        if ret != 0:
                print('======quantization transfer 10000 error !!===========')
        else:
                print('======quantization transfer 10000 ok !!===========')

