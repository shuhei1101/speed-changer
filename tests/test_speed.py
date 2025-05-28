import pytest
from speed_changer.speed import Speed


class TestSpeed:
    def test_0_5で初期化できること(self):
        speed = Speed(0.5)
        assert str(speed) == "attempo=0.5"

    def test_2_0で初期化できること(self):
        speed = Speed(2.0)
        assert str(speed) == "attempo=2.0"

    def test_0_5未満で初期化できないこと(self):
        with pytest.raises(ValueError, match="速度は0.5から2.0の間で指定してください"):
            Speed(0.4)

    def test_2_0を超えて初期化できないこと(self):
        with pytest.raises(ValueError, match="速度は0.5から2.0の間で指定してください"):
            Speed(2.1)

    def test_string変換が正しいこと(self):
        speed = Speed(1.5)
        assert str(speed) == "attempo=1.5"
