"""
flet kullanılacak. kullanıcı girecek. iki tarih aralığı ve parite seçecek.
grafik olarak mum grafiği oluşturulacak. 5 dk ve 10 dk 1 saat gibi seçenekler olacak. verileri çekecek.


"""
import flet as ft
import yfinance as yf
import plotly.graph_objects as go


def main(page: ft.Page):
    page.title = "Mum Grafiği Uygulaması"
    page.scroll = True

    parite = ft.Dropdown(
        label="Parite Seçin",
        options=[
            ft.dropdown.Option("EURUSD=X"),
            ft.dropdown.Option("GBPUSD=X"),
            ft.dropdown.Option("BTC-USD"),
            ft.dropdown.Option("ETH-USD"),
        ],
        width=200
    )

    zaman_dilimi = ft.Dropdown(
        label="Zaman Dilimi",
        options=[
            ft.dropdown.Option("5m"),
            ft.dropdown.Option("10m"),
            ft.dropdown.Option("60m"),
            ft.dropdown.Option("240m"),
            ft.dropdown.Option("1d"),
        ],
        width=200
    )

    baslangic = ft.TextField(label="Başlangıç Tarihi (YYYY-MM-DD)", width=200)
    bitis = ft.TextField(label="Bitiş Tarihi (YYYY-MM-DD)", width=200)

    grafik_area = ft.PlotlyChart(
        figure=go.Figure(),
        expand=True,
        height=600
    )

    def grafik_getir(e):
        try:
            data = yf.download(
                parite.value,
                start=baslangic.value,
                end=bitis.value,
                interval=zaman_dilimi.value
            )

            if data.empty:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Veri alınamadı! Tarih aralığını veya pariteyi kontrol edin."),
                )
                page.snack_bar.open = True
                page.update()
                return

            fig = go.Figure(data=[
                go.Candlestick(
                    x=data.index,
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"]
                )
            ])

            fig.update_layout(
                title=f"{parite.value} Mum Grafiği",
                xaxis_title="Tarih",
                yaxis_title="Fiyat"
            )

            grafik_area.figure = fig
            page.update()

        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Hata: {err}"))
            page.snack_bar.open = True
            page.update()

    getir_buton = ft.ElevatedButton("Grafiği Getir", on_click=grafik_getir)

    page.add(
        ft.Row([parite, zaman_dilimi]),
        ft.Row([baslangic, bitis]),
        getir_buton,
        grafik_area
    )


ft.app(main)
