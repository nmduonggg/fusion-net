python train_SuperNet.py \
    --template SuperNet_4s \
    --lbda 0.0 \
    --gamma 0.0 \
    --den_target 0.7 \
    --tile 1 \
    --cv_dir checkpoints/SUPERNET \
    --nblocks 1 \
    --lr 0.00001
    # --max_load 1000