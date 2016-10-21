speedtest-chart
======================
Script Python đẩy dữ kết qủa check network (Sử dụng speedtest-cli) về Google Docs spreasheet. Các thông số gồm upload, download và latency


Có thể xem demo tại: https://docs.google.com/spreadsheets/d/1QvV6POBVBXuq5iXSOLNd5bwgd5To8FMuvsrSfvY7Nuk/pubchart?oid=1973311741&format=interactive

### Yêu cầu

* Python 2.6
* [`speedtest-cli`](https://github.com/sivel/speedtest-cli)
* Google account

### Cài đặt và sử dung

1. Clone va open repository:  
  `git clone https://github.com/dangngovan/speedtest-chart.git && cd speedtest-chart`
1. Cài đặt các công cụ liên quan :  
  `pip install gdata speedtest-cli google-api-python-client`
1. Tại file cấu hình:  
  `cp default.config.json config.json``
1. Tạo một OAuth token theo hướng dẫn:  
  :book: [docs/How-to-create-a-Google-OAuth-token.md](docs/How-to-create-a-Google-OAuth-token.md)
1. Tạo một spreadsheet và lấy kết qủa:  
  :book: [docs/Create-a-spreadsheet-to-collect-data.md](docs/Create-a-spreadsheet-to-collect-data.md) and make sure to adjust `spreadsheet_id` in the `config.json` file
1. Chạy cript :  
  `$ python speetest.py

### License

[MIT](LICENSE)

### Version

1.3.1
# speedtest-chart
