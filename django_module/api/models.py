from django.db import models


# Create your models here.
class TelegramUsers(models.Model):
    chat_id = models.CharField(max_length=20, default=None, unique=True)
    username = models.CharField(max_length=20, default=None, unique=True, primary_key=True)


class Funding(models.Model):
    symbol = models.CharField(max_length=12, default=None, unique=True, primary_key=True)
    exchangeLogo = models.CharField(max_length=120, default="")
    binance_funding = models.FloatField(default=0.00)
    okx_funding = models.FloatField(default=0.00)
    dydx_funding = models.FloatField(default=0.00)
    bybit_funding = models.FloatField(default=0.00)
    gate_funding = models.FloatField(default=0.00)
    bitget_funding = models.FloatField(default=0.00)
    coinex_funding = models.FloatField(default=0.00)
    bingx_funding = models.FloatField(default=0.00)
    other_exchange_sum = models.FloatField(default=0.00)


class FundingFinal(models.Model):
    symbol = models.CharField(max_length=12, default=None, unique=True, primary_key=True)
    binance_positive = models.IntegerField(default=0)
    binance_balance = models.IntegerField(default=0)
    binance_negative = models.IntegerField(default=0)
    other_ex_positive = models.IntegerField(default=0)
    other_ex_balance = models.IntegerField(default=0)
    other_ex_negative = models.IntegerField(default=0)


class FundingTop10Pos(models.Model):
    pos_symbol = models.CharField(max_length=10, default="")
    pos_value = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # Обрезаем значение поля до 6 символов перед сохранением
        self.pos_symbol = self.pos_symbol[:6]
        super().save(*args, **kwargs)


class FundingTop10Neg(models.Model):
    neg_symbol = models.CharField(max_length=10, default="")
    neg_value = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # Обрезаем значение поля до 6 символов перед сохранением
        self.neg_symbol = self.neg_symbol[:6]
        super().save(*args, **kwargs)

