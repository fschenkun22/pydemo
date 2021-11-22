# 阿尔法接口

## 地址：127.0.0.1:65500/get/
## 请求方式 ： get获取，put写入
##### <em>返回json里 code=200为操作成功，其余全部失败</em>

### 示例：GET：http://127.0.0.1:65500/get/20211015-003
``` {
    "code": "200",
    "command_loopback": "/get/20211015-003",
    "contract_num": "20211015-003",
    "detail": "success",
    "result": {
        "header_detail": {
            "JobID": 4928,
            "JobNo": "代理商测试-211015001",
            "JobName": "测试订单名称2",
            "Client": "客户名称测试",
            "OrderDate": "2021-10-15 00:00:00",
            "Address": "安装地址测试",
            "LinkMan": "15641366461",
            "Memo": "",
            "Tel": "15641366461",
            "IsLock": false,
            "State": 10,
            "Area": 8.2653,
            "Barcode": "21100001"
        },
        "parts": {
            "1": {
                "JPID": 24305,
                "ProductName2": "地柜B1",
                "Width": 900.0,
                "Depth": 550.0,
                "Height": 680.0,
                "Memo": "",
                "panels": {
                    "0": {
                        "id": 592691,
                        "JPID": 24305,
                        "PanleName2": "拉带",
                        "Barcode": "00592691",
                        "Length": 864.0,
                        "Width": 60.0,
                        "EBL1": "0.8*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "1": {
                        "id": 592692,
                        "JPID": 24305,
                        "PanleName2": "拉带",
                        "Barcode": "00592692",
                        "Length": 864.0,
                        "Width": 60.0,
                        "EBL1": "0.8*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "2": {
                        "id": 592693,
                        "JPID": 24305,
                        "PanleName2": "左侧",
                        "Barcode": "00592693",
                        "Length": 680.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "3": {
                        "id": 592694,
                        "JPID": 24305,
                        "PanleName2": "右侧",
                        "Barcode": "00592694",
                        "Length": 680.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽6 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "4": {
                        "id": 592695,
                        "JPID": 24305,
                        "PanleName2": "底板",
                        "Barcode": "00592695",
                        "Length": 864.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 通槽",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "5": {
                        "id": 592696,
                        "JPID": 24305,
                        "PanleName2": "薄背",
                        "Barcode": "00592696",
                        "Length": 627.0,
                        "Width": 874.0,
                        "EBL1": "",
                        "EBL2": "",
                        "EBW1": "",
                        "EBW2": "",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7502,
                            "MaterName": "5板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 5.0,
                            "Material": "板"
                        }
                    },
                    "6": {
                        "id": 592697,
                        "JPID": 24305,
                        "PanleName2": "活层",
                        "Barcode": "00592697",
                        "Length": 862.0,
                        "Width": 516.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    }
                },
                "hardwares": {
                    "0": {
                        "id": 2581564,
                        "JPID": 24305,
                        "WJName2": "铝边条"
                    },
                    "1": {
                        "id": 2581565,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "2": {
                        "id": 2581566,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "3": {
                        "id": 2581567,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "4": {
                        "id": 2581568,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "5": {
                        "id": 2581569,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "6": {
                        "id": 2581570,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "7": {
                        "id": 2581571,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "8": {
                        "id": 2581572,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "9": {
                        "id": 2581585,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "10": {
                        "id": 2581586,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "11": {
                        "id": 2581587,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "12": {
                        "id": 2581588,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "13": {
                        "id": 2581589,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "14": {
                        "id": 2581590,
                        "JPID": 24305,
                        "WJName2": "三合一"
                    },
                    "15": {
                        "id": 2581591,
                        "JPID": 24305,
                        "WJName2": "橱柜调节脚"
                    },
                    "16": {
                        "id": 2581592,
                        "JPID": 24305,
                        "WJName2": "层板钉"
                    },
                    "17": {
                        "id": 2581593,
                        "JPID": 24305,
                        "WJName2": "层板钉"
                    },
                    "18": {
                        "id": 2581594,
                        "JPID": 24305,
                        "WJName2": "层板钉"
                    },
                    "19": {
                        "id": 2581595,
                        "JPID": 24305,
                        "WJName2": "层板钉"
                    }
                }
            },
            "2": {
                "JPID": 24306,
                "ProductName2": "吊柜W2",
                "Width": 600.0,
                "Depth": 330.0,
                "Height": 720.0,
                "Memo": "开槽",
                "panels": {
                    "0": {
                        "id": 592698,
                        "JPID": 24306,
                        "PanleName2": "顶板",
                        "Barcode": "00592698",
                        "Length": 564.0,
                        "Width": 330.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽6 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "1": {
                        "id": 592699,
                        "JPID": 24306,
                        "PanleName2": "左侧",
                        "Barcode": "00592699",
                        "Length": 720.0,
                        "Width": 330.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "2": {
                        "id": 592700,
                        "JPID": 24306,
                        "PanleName2": "右侧",
                        "Barcode": "00592700",
                        "Length": 702.0,
                        "Width": 330.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽6 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "3": {
                        "id": 592701,
                        "JPID": 24306,
                        "PanleName2": "底板",
                        "Barcode": "00592701",
                        "Length": 64.0,
                        "Width": 330.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 通槽",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "4": {
                        "id": 592702,
                        "JPID": 24306,
                        "PanleName2": "薄背",
                        "Barcode": "00592702",
                        "Length": 694.0,
                        "Width": 74.0,
                        "EBL1": "",
                        "EBL2": "",
                        "EBW1": "",
                        "EBW2": "",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7502,
                            "MaterName": "5板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 5.0,
                            "Material": "板"
                        }
                    },
                    "5": {
                        "id": 592703,
                        "JPID": 24306,
                        "PanleName2": "活层",
                        "Barcode": "00592703",
                        "Length": 62.0,
                        "Width": 296.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "6": {
                        "id": 592704,
                        "JPID": 24306,
                        "PanleName2": "左侧",
                        "Barcode": "00592704",
                        "Length": 702.0,
                        "Width": 330.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "7": {
                        "id": 592705,
                        "JPID": 24306,
                        "PanleName2": "右侧",
                        "Barcode": "00592705",
                        "Length": 720.0,
                        "Width": 330.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽6 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "8": {
                        "id": 592706,
                        "JPID": 24306,
                        "PanleName2": "活层",
                        "Barcode": "00592706",
                        "Length": 62.0,
                        "Width": 296.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "9": {
                        "id": 592707,
                        "JPID": 24306,
                        "PanleName2": "底板",
                        "Barcode": "00592707",
                        "Length": 64.0,
                        "Width": 330.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 通槽",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "10": {
                        "id": 592708,
                        "JPID": 24306,
                        "PanleName2": "薄背",
                        "Barcode": "00592708",
                        "Length": 694.0,
                        "Width": 74.0,
                        "EBL1": "",
                        "EBL2": "",
                        "EBW1": "",
                        "EBW2": "",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7502,
                            "MaterName": "5板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 5.0,
                            "Material": "板"
                        }
                    }
                },
                "hardwares": {
                    "0": {
                        "id": 2581596,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "1": {
                        "id": 2581597,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "2": {
                        "id": 2581598,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "3": {
                        "id": 2581599,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "4": {
                        "id": 2581604,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "5": {
                        "id": 2581605,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "6": {
                        "id": 2581608,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "7": {
                        "id": 2581609,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "8": {
                        "id": 2581610,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "9": {
                        "id": 2581611,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "10": {
                        "id": 2581612,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "11": {
                        "id": 2581613,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "12": {
                        "id": 2581614,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "13": {
                        "id": 2581615,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "14": {
                        "id": 2581616,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "15": {
                        "id": 2581617,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "16": {
                        "id": 2581624,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "17": {
                        "id": 2581625,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "18": {
                        "id": 2581626,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "19": {
                        "id": 2581627,
                        "JPID": 24306,
                        "WJName2": "层板钉"
                    },
                    "20": {
                        "id": 2581628,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "21": {
                        "id": 2581629,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "22": {
                        "id": 2581630,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    },
                    "23": {
                        "id": 2581631,
                        "JPID": 24306,
                        "WJName2": "三合一"
                    }
                }
            },
            "3": {
                "JPID": 24308,
                "ProductName2": "地柜B3",
                "Width": 900.0,
                "Depth": 550.0,
                "Height": 680.0,
                "Memo": "",
                "panels": {
                    "0": {
                        "id": 592709,
                        "JPID": 24308,
                        "PanleName2": "拉带",
                        "Barcode": "00592709",
                        "Length": 864.0,
                        "Width": 60.0,
                        "EBL1": "0.8*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "1": {
                        "id": 592710,
                        "JPID": 24308,
                        "PanleName2": "拉带",
                        "Barcode": "00592710",
                        "Length": 864.0,
                        "Width": 60.0,
                        "EBL1": "0.8*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "2": {
                        "id": 592711,
                        "JPID": 24308,
                        "PanleName2": "左侧",
                        "Barcode": "00592711",
                        "Length": 680.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "3": {
                        "id": 592712,
                        "JPID": 24308,
                        "PanleName2": "右侧",
                        "Barcode": "00592712",
                        "Length": 680.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽6 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "4": {
                        "id": 592713,
                        "JPID": 24308,
                        "PanleName2": "底板",
                        "Barcode": "00592713",
                        "Length": 864.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 通槽",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "5": {
                        "id": 592714,
                        "JPID": 24308,
                        "PanleName2": "薄背",
                        "Barcode": "00592714",
                        "Length": 627.0,
                        "Width": 874.0,
                        "EBL1": "",
                        "EBL2": "",
                        "EBW1": "",
                        "EBW2": "",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7502,
                            "MaterName": "5板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 5.0,
                            "Material": "板"
                        }
                    },
                    "6": {
                        "id": 592715,
                        "JPID": 24308,
                        "PanleName2": "活层",
                        "Barcode": "00592715",
                        "Length": 862.0,
                        "Width": 516.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    }
                },
                "hardwares": {
                    "0": {
                        "id": 2581632,
                        "JPID": 24308,
                        "WJName2": "铝边条"
                    },
                    "1": {
                        "id": 2581633,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "2": {
                        "id": 2581634,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "3": {
                        "id": 2581635,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "4": {
                        "id": 2581636,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "5": {
                        "id": 2581637,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "6": {
                        "id": 2581638,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "7": {
                        "id": 2581639,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "8": {
                        "id": 2581640,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "9": {
                        "id": 2581653,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "10": {
                        "id": 2581654,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "11": {
                        "id": 2581655,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "12": {
                        "id": 2581656,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "13": {
                        "id": 2581657,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "14": {
                        "id": 2581658,
                        "JPID": 24308,
                        "WJName2": "三合一"
                    },
                    "15": {
                        "id": 2581659,
                        "JPID": 24308,
                        "WJName2": "橱柜调节脚"
                    },
                    "16": {
                        "id": 2581660,
                        "JPID": 24308,
                        "WJName2": "层板钉"
                    },
                    "17": {
                        "id": 2581661,
                        "JPID": 24308,
                        "WJName2": "层板钉"
                    },
                    "18": {
                        "id": 2581662,
                        "JPID": 24308,
                        "WJName2": "层板钉"
                    },
                    "19": {
                        "id": 2581663,
                        "JPID": 24308,
                        "WJName2": "层板钉"
                    }
                }
            },
            "4": {
                "JPID": 24309,
                "ProductName2": "地柜B4",
                "Width": 900.0,
                "Depth": 550.0,
                "Height": 680.0,
                "Memo": "",
                "panels": {
                    "0": {
                        "id": 592716,
                        "JPID": 24309,
                        "PanleName2": "拉带",
                        "Barcode": "00592716",
                        "Length": 864.0,
                        "Width": 60.0,
                        "EBL1": "0.8*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "1": {
                        "id": 592717,
                        "JPID": 24309,
                        "PanleName2": "拉带",
                        "Barcode": "00592717",
                        "Length": 864.0,
                        "Width": 60.0,
                        "EBL1": "0.8*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "2": {
                        "id": 592718,
                        "JPID": 24309,
                        "PanleName2": "左侧",
                        "Barcode": "00592718",
                        "Length": 680.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "3": {
                        "id": 592719,
                        "JPID": 24309,
                        "PanleName2": "右侧",
                        "Barcode": "00592719",
                        "Length": 680.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽6 内槽|C",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "4": {
                        "id": 592720,
                        "JPID": 24309,
                        "PanleName2": "底板",
                        "Barcode": "00592720",
                        "Length": 864.0,
                        "Width": 550.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "|槽5 通槽",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    },
                    "5": {
                        "id": 592721,
                        "JPID": 24309,
                        "PanleName2": "薄背",
                        "Barcode": "00592721",
                        "Length": 627.0,
                        "Width": 874.0,
                        "EBL1": "",
                        "EBL2": "",
                        "EBW1": "",
                        "EBW2": "",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7502,
                            "MaterName": "5板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 5.0,
                            "Material": "板"
                        }
                    },
                    "6": {
                        "id": 592722,
                        "JPID": 24309,
                        "PanleName2": "活层",
                        "Barcode": "00592722",
                        "Length": 862.0,
                        "Width": 516.0,
                        "EBL1": "1.5*22欧洲胡桃",
                        "EBL2": "0.8*22欧洲胡桃",
                        "EBW1": "0.8*22欧洲胡桃",
                        "EBW2": "0.8*22欧洲胡桃",
                        "Memo": "",
                        "IsPackScan": null,
                        "Material": {
                            "MaterID": 7586,
                            "MaterName": "18板欧洲胡桃",
                            "Color": "欧洲胡桃",
                            "Thickness": 18.0,
                            "Material": "板"
                        }
                    }
                },
                "hardwares": {
                    "0": {
                        "id": 2581664,
                        "JPID": 24309,
                        "WJName2": "铝边条"
                    },
                    "1": {
                        "id": 2581665,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "2": {
                        "id": 2581666,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "3": {
                        "id": 2581667,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "4": {
                        "id": 2581668,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "5": {
                        "id": 2581669,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "6": {
                        "id": 2581670,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "7": {
                        "id": 2581671,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "8": {
                        "id": 2581672,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "9": {
                        "id": 2581685,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "10": {
                        "id": 2581686,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "11": {
                        "id": 2581687,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "12": {
                        "id": 2581688,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "13": {
                        "id": 2581689,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "14": {
                        "id": 2581690,
                        "JPID": 24309,
                        "WJName2": "三合一"
                    },
                    "15": {
                        "id": 2581691,
                        "JPID": 24309,
                        "WJName2": "橱柜调节脚"
                    },
                    "16": {
                        "id": 2581692,
                        "JPID": 24309,
                        "WJName2": "层板钉"
                    },
                    "17": {
                        "id": 2581693,
                        "JPID": 24309,
                        "WJName2": "层板钉"
                    },
                    "18": {
                        "id": 2581694,
                        "JPID": 24309,
                        "WJName2": "层板钉"
                    },
                    "19": {
                        "id": 2581695,
                        "JPID": 24309,
                        "WJName2": "层板钉"
                    }
                }
            }
        },
        "money": {
            "1": {
                "JPID": 24305,
                "ID": 592691,
                "ProductName2": "地柜B1",
                "ItemName": "拉带",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0518,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 60.0
            },
            "2": {
                "JPID": 24305,
                "ID": 592692,
                "ProductName2": "地柜B1",
                "ItemName": "拉带",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0518,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 60.0
            },
            "3": {
                "JPID": 24305,
                "ID": 592693,
                "ProductName2": "地柜B1",
                "ItemName": "左侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.374,
                "Price": 120.0,
                "Length": 680.0,
                "Width": 550.0
            },
            "4": {
                "JPID": 24305,
                "ID": 592694,
                "ProductName2": "地柜B1",
                "ItemName": "右侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.374,
                "Price": 120.0,
                "Length": 680.0,
                "Width": 550.0
            },
            "5": {
                "JPID": 24305,
                "ID": 592695,
                "ProductName2": "地柜B1",
                "ItemName": "底板",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.4752,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 550.0
            },
            "6": {
                "JPID": 24305,
                "ID": 592696,
                "ProductName2": "地柜B1",
                "ItemName": "薄背",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "5板欧洲胡桃",
                "Qty": 0.548,
                "Price": 60.0,
                "Length": 627.0,
                "Width": 874.0
            },
            "7": {
                "JPID": 24305,
                "ID": 592697,
                "ProductName2": "地柜B1",
                "ItemName": "活层",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.4448,
                "Price": 120.0,
                "Length": 862.0,
                "Width": 516.0
            },
            "8": {
                "JPID": 24305,
                "ID": 0,
                "ProductName2": "地柜B1",
                "ItemName": "mm",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "铝边条",
                "Qty": 0.862,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "9": {
                "JPID": 24305,
                "ID": 0,
                "ProductName2": "地柜B1",
                "ItemName": "个",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "层板钉",
                "Qty": 4.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "10": {
                "JPID": 24305,
                "ID": 0,
                "ProductName2": "地柜B1",
                "ItemName": "个",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "橱柜调节脚",
                "Qty": 4.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "11": {
                "JPID": 24305,
                "ID": 0,
                "ProductName2": "地柜B1",
                "ItemName": "套",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "三合一",
                "Qty": 14.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "12": {
                "JPID": 24305,
                "ID": 0,
                "ProductName2": "地柜B1",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "0.8*22欧洲胡桃",
                "Qty": 11.514,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "13": {
                "JPID": 24305,
                "ID": 0,
                "ProductName2": "地柜B1",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "1.5*22欧洲胡桃",
                "Qty": 3.166,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "14": {
                "JPID": 24306,
                "ID": 592698,
                "ProductName2": "吊柜W2",
                "ItemName": "顶板",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.1861,
                "Price": 120.0,
                "Length": 564.0,
                "Width": 330.0
            },
            "15": {
                "JPID": 24306,
                "ID": 592699,
                "ProductName2": "吊柜W2",
                "ItemName": "左侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.2376,
                "Price": 120.0,
                "Length": 720.0,
                "Width": 330.0
            },
            "16": {
                "JPID": 24306,
                "ID": 592700,
                "ProductName2": "吊柜W2",
                "ItemName": "右侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.2317,
                "Price": 120.0,
                "Length": 702.0,
                "Width": 330.0
            },
            "17": {
                "JPID": 24306,
                "ID": 592701,
                "ProductName2": "吊柜W2",
                "ItemName": "底板",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0211,
                "Price": 120.0,
                "Length": 64.0,
                "Width": 330.0
            },
            "18": {
                "JPID": 24306,
                "ID": 592702,
                "ProductName2": "吊柜W2",
                "ItemName": "薄背",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "5板欧洲胡桃",
                "Qty": 0.0514,
                "Price": 60.0,
                "Length": 694.0,
                "Width": 74.0
            },
            "19": {
                "JPID": 24306,
                "ID": 592703,
                "ProductName2": "吊柜W2",
                "ItemName": "活层",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0184,
                "Price": 120.0,
                "Length": 62.0,
                "Width": 296.0
            },
            "20": {
                "JPID": 24306,
                "ID": 592704,
                "ProductName2": "吊柜W2",
                "ItemName": "左侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.2317,
                "Price": 120.0,
                "Length": 702.0,
                "Width": 330.0
            },
            "21": {
                "JPID": 24306,
                "ID": 592705,
                "ProductName2": "吊柜W2",
                "ItemName": "右侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.2376,
                "Price": 120.0,
                "Length": 720.0,
                "Width": 330.0
            },
            "22": {
                "JPID": 24306,
                "ID": 592706,
                "ProductName2": "吊柜W2",
                "ItemName": "活层",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0184,
                "Price": 120.0,
                "Length": 62.0,
                "Width": 296.0
            },
            "23": {
                "JPID": 24306,
                "ID": 592707,
                "ProductName2": "吊柜W2",
                "ItemName": "底板",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0211,
                "Price": 120.0,
                "Length": 64.0,
                "Width": 330.0
            },
            "24": {
                "JPID": 24306,
                "ID": 592708,
                "ProductName2": "吊柜W2",
                "ItemName": "薄背",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "5板欧洲胡桃",
                "Qty": 0.0514,
                "Price": 60.0,
                "Length": 694.0,
                "Width": 74.0
            },
            "25": {
                "JPID": 24306,
                "ID": 0,
                "ProductName2": "吊柜W2",
                "ItemName": "个",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "层板钉",
                "Qty": 8.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "26": {
                "JPID": 24306,
                "ID": 0,
                "ProductName2": "吊柜W2",
                "ItemName": "套",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "三合一",
                "Qty": 16.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "27": {
                "JPID": 24306,
                "ID": 0,
                "ProductName2": "吊柜W2",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "0.8*22欧洲胡桃",
                "Qty": 10.004,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "28": {
                "JPID": 24306,
                "ID": 0,
                "ProductName2": "吊柜W2",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "1.5*22欧洲胡桃",
                "Qty": 3.84,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "29": {
                "JPID": 24308,
                "ID": 592709,
                "ProductName2": "地柜B3",
                "ItemName": "拉带",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0518,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 60.0
            },
            "30": {
                "JPID": 24308,
                "ID": 592710,
                "ProductName2": "地柜B3",
                "ItemName": "拉带",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0518,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 60.0
            },
            "31": {
                "JPID": 24308,
                "ID": 592711,
                "ProductName2": "地柜B3",
                "ItemName": "左侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.374,
                "Price": 120.0,
                "Length": 680.0,
                "Width": 550.0
            },
            "32": {
                "JPID": 24308,
                "ID": 592712,
                "ProductName2": "地柜B3",
                "ItemName": "右侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.374,
                "Price": 120.0,
                "Length": 680.0,
                "Width": 550.0
            },
            "33": {
                "JPID": 24308,
                "ID": 592713,
                "ProductName2": "地柜B3",
                "ItemName": "底板",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.4752,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 550.0
            },
            "34": {
                "JPID": 24308,
                "ID": 592714,
                "ProductName2": "地柜B3",
                "ItemName": "薄背",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "5板欧洲胡桃",
                "Qty": 0.548,
                "Price": 60.0,
                "Length": 627.0,
                "Width": 874.0
            },
            "35": {
                "JPID": 24308,
                "ID": 592715,
                "ProductName2": "地柜B3",
                "ItemName": "活层",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.4448,
                "Price": 120.0,
                "Length": 862.0,
                "Width": 516.0
            },
            "36": {
                "JPID": 24308,
                "ID": 0,
                "ProductName2": "地柜B3",
                "ItemName": "mm",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "铝边条",
                "Qty": 0.862,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "37": {
                "JPID": 24308,
                "ID": 0,
                "ProductName2": "地柜B3",
                "ItemName": "个",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "层板钉",
                "Qty": 4.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "38": {
                "JPID": 24308,
                "ID": 0,
                "ProductName2": "地柜B3",
                "ItemName": "个",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "橱柜调节脚",
                "Qty": 4.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "39": {
                "JPID": 24308,
                "ID": 0,
                "ProductName2": "地柜B3",
                "ItemName": "套",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "三合一",
                "Qty": 14.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "40": {
                "JPID": 24308,
                "ID": 0,
                "ProductName2": "地柜B3",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "0.8*22欧洲胡桃",
                "Qty": 11.514,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "41": {
                "JPID": 24308,
                "ID": 0,
                "ProductName2": "地柜B3",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "1.5*22欧洲胡桃",
                "Qty": 3.166,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "42": {
                "JPID": 24309,
                "ID": 592716,
                "ProductName2": "地柜B4",
                "ItemName": "拉带",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0518,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 60.0
            },
            "43": {
                "JPID": 24309,
                "ID": 592717,
                "ProductName2": "地柜B4",
                "ItemName": "拉带",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.0518,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 60.0
            },
            "44": {
                "JPID": 24309,
                "ID": 592718,
                "ProductName2": "地柜B4",
                "ItemName": "左侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.374,
                "Price": 120.0,
                "Length": 680.0,
                "Width": 550.0
            },
            "45": {
                "JPID": 24309,
                "ID": 592719,
                "ProductName2": "地柜B4",
                "ItemName": "右侧",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.374,
                "Price": 120.0,
                "Length": 680.0,
                "Width": 550.0
            },
            "46": {
                "JPID": 24309,
                "ID": 592720,
                "ProductName2": "地柜B4",
                "ItemName": "底板",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.4752,
                "Price": 120.0,
                "Length": 864.0,
                "Width": 550.0
            },
            "47": {
                "JPID": 24309,
                "ID": 592721,
                "ProductName2": "地柜B4",
                "ItemName": "薄背",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "5板欧洲胡桃",
                "Qty": 0.548,
                "Price": 60.0,
                "Length": 627.0,
                "Width": 874.0
            },
            "48": {
                "JPID": 24309,
                "ID": 592722,
                "ProductName2": "地柜B4",
                "ItemName": "活层",
                "Discount": 1.0,
                "CateID": 1,
                "Category": "双饰面板",
                "Name": "18板欧洲胡桃",
                "Qty": 0.4448,
                "Price": 120.0,
                "Length": 862.0,
                "Width": 516.0
            },
            "49": {
                "JPID": 24309,
                "ID": 0,
                "ProductName2": "地柜B4",
                "ItemName": "mm",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "铝边条",
                "Qty": 0.862,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "50": {
                "JPID": 24309,
                "ID": 0,
                "ProductName2": "地柜B4",
                "ItemName": "个",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "层板钉",
                "Qty": 4.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "51": {
                "JPID": 24309,
                "ID": 0,
                "ProductName2": "地柜B4",
                "ItemName": "个",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "橱柜调节脚",
                "Qty": 4.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "52": {
                "JPID": 24309,
                "ID": 0,
                "ProductName2": "地柜B4",
                "ItemName": "套",
                "Discount": 1.0,
                "CateID": 2,
                "Category": "五金",
                "Name": "三合一",
                "Qty": 14.0,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "53": {
                "JPID": 24309,
                "ID": 0,
                "ProductName2": "地柜B4",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "0.8*22欧洲胡桃",
                "Qty": 11.514,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            },
            "54": {
                "JPID": 24309,
                "ID": 0,
                "ProductName2": "地柜B4",
                "ItemName": "",
                "Discount": 1.0,
                "CateID": 3,
                "Category": "封边材料",
                "Name": "1.5*22欧洲胡桃",
                "Qty": 3.166,
                "Price": 0,
                "Length": 1.0,
                "Width": 1.0
            }
        }
    }
}
```
### 示例：PUT：http://127.0.0.1:65500?PactNo=B211115-001WB-1-1&JobNo=20211110单号测试&JobName=订单名称测试&Client=客户名称测试&OrderDate=now&Address=安装地址测试&LinkMan=联系人测试&Memo=备注测试&Tel=15641366461&GUID=random&Designer=设计师测试&Calculator=拆单1&Dealer=代理商名测试&Write_enable=test
### <em>Write_enable=test时为测试写入，Write_enable=55aa时为真写入</em>
```
{
    "code": 200,
    "status": true,
    "msg": "write done"
}
```