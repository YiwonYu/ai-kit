"""실행 도구 검증용 예제. 실제 과제 알고리즘이 아니다."""
import argparse
import os
import random
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('--mode', choices=['success', 'fail', 'wait'], default='success')
a = p.parse_args()
random.seed(int(os.environ.get('HARNESS_SEED', '0')))
print('demo started', flush=True)
if a.mode == 'wait':
    time.sleep(10)
if a.mode == 'fail':
    print('intentional failure', file=sys.stderr, flush=True)
    sys.exit(7)
print('demo result:', random.randint(0, 100), flush=True)
