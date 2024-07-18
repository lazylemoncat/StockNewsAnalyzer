import pytest

from main import get_xlcj_gzmt_response

@pytest.fixture
def get_xlcj_gzmt_response():
  return get_xlcj_gzmt_response()

def test_get_xlcj_gzmt_response():
  response = get_xlcj_gzmt_response()
  assert response.status_code == 200
  assert response.encoding == 'gbk'

if __name__ == '__main__':
  pytest.main(['-s', 'test.py'])