"""Real-ESRGAN x4plus (RRDBNet) inference in plain numpy, loading the official .pth without torch."""
import zipfile, pickle, numpy as np, sys, time
from PIL import Image

def load_pth(path):
    z = zipfile.ZipFile(path); root = z.namelist()[0].split('/')[0]
    class Storage:
        def __init__(self, key, dtype): self.key, self.dtype = key, dtype
    DT = {'FloatStorage': np.float32, 'HalfStorage': np.float16, 'DoubleStorage': np.float64, 'LongStorage': np.int64}
    def rebuild(storage, offset, size, stride, *a):
        buf = np.frombuffer(z.read(f'{root}/data/{storage.key}'), dtype=storage.dtype)
        n = int(np.prod(size)) if size else 1
        if not size: return buf[offset].copy()
        return np.lib.stride_tricks.as_strided(buf[offset:], shape=size, strides=[s * buf.itemsize for s in stride]).astype(np.float32).copy()
    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if name == '_rebuild_tensor_v2': return rebuild
            if mod == 'collections' and name == 'OrderedDict':
                import collections; return collections.OrderedDict
            if name.endswith('Storage'): return name
            return super().find_class(mod, name)
        def persistent_load(self, pid):
            _, stype, key, loc, numel = pid
            return Storage(key, DT[stype if isinstance(stype, str) else stype.__name__])
    sd = U(z.open(f'{root}/data.pkl')).load()
    return sd.get('params_ema', sd.get('params', sd))

def conv3(x, w, b, band=96):
    """x: (C,H,W) float32; w: (O,C,3,3); same padding. Row bands keep memory small."""
    C, H, W = x.shape; O = w.shape[0]
    wm = w.reshape(O, C * 9).T
    xp = np.pad(x, ((0, 0), (1, 1), (1, 1)))
    out = np.empty((O, H, W), np.float32)
    for y0 in range(0, H, band):
        y1 = min(H, y0 + band)
        win = np.lib.stride_tricks.sliding_window_view(xp[:, y0:y1 + 2], (3, 3), axis=(1, 2))  # C, h, W, 3, 3
        cols = win.transpose(1, 2, 0, 3, 4).reshape((y1 - y0) * W, C * 9)
        out[:, y0:y1] = (cols @ wm + b).T.reshape(O, y1 - y0, W)
    return out

lrelu = lambda x: np.where(x > 0, x, 0.2 * x).astype(np.float32)
up2 = lambda x: x.repeat(2, axis=1).repeat(2, axis=2)

def run(P, img):
    c = lambda name, x: conv3(x, P[name + '.weight'], P[name + '.bias'])
    x = np.asarray(img, np.float32).transpose(2, 0, 1) / 255.0
    feat = c('conv_first', x); body = feat
    for i in range(23):
        rr = body
        for r in ('rdb1', 'rdb2', 'rdb3'):
            p = f'body.{i}.{r}.'; x0 = rr
            x1 = lrelu(c(p + 'conv1', x0)); x2 = lrelu(c(p + 'conv2', np.concatenate([x0, x1])))
            x3 = lrelu(c(p + 'conv3', np.concatenate([x0, x1, x2]))); x4 = lrelu(c(p + 'conv4', np.concatenate([x0, x1, x2, x3])))
            x5 = c(p + 'conv5', np.concatenate([x0, x1, x2, x3, x4])); rr = x5 * 0.2 + x0
        body = rr * 0.2 + body
    feat = feat + c('conv_body', body)
    feat = lrelu(c('conv_up1', up2(feat))); feat = lrelu(c('conv_up2', up2(feat)))
    out = c('conv_last', lrelu(c('conv_hr', feat)))
    return Image.fromarray((np.clip(out, 0, 1).transpose(1, 2, 0) * 255 + 0.5).astype(np.uint8))

if __name__ == '__main__':
    P = load_pth(sys.argv[1])
    for src, dst in zip(sys.argv[2::2], sys.argv[3::2]):
        t = time.time(); im = Image.open(src).convert('RGB'); run(P, im).save(dst); print(src, im.size, f'{time.time()-t:.0f}s', flush=True)
