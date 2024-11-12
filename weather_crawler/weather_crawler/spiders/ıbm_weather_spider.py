import datetime
import re
import scrapy
from weather_crawler.items import WeatherCrawlerItem


class havadurumux_spiders(scrapy.Spider):
    name = 'ibm'
    # # XPath rules  (city, highest temperature, lowest temperature, date, weather information)
    ıbm_json = {
        "ıbm_city": "//h1/span/span/text() | //*[@id='WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034']/div/section/div/div/div[1]/h1/text()",
        "ıbm_up": ".//div/div/div[2]/span[1]/text()",
        "ıbm_low": "//*[@id='WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034']/div/section/div/div/div[2]/div[1]/div[1]/div[2]/span[2]/text() |.//div/div/div[2]/span[2]/span/text() ",
        "ıbm_date": ".//div/div/h3/text()",
        "ıbm_objects": "/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/div[2]/details",
        "ıbm_delete_pattern": "(\d+)"
    }

    # Provincial plate codes and weather links
    provincial_plate = {
        1: 'https://weather.com/tr-TR/weather/tenday/l/759de7bce739bffeb0afb067e2292689c5e5c639ab58fee51064105554d9e294',
        2: 'https://weather.com/tr-TR/weather/tenday/l/e840d5313628355d0b0fcdffc4cefb5e21d6574cb44be670d7a3c5c4c6ca34fc',
        3: 'https://weather.com/tr-TR/weather/tenday/l/6915a0e957b64d10795353b30fca3378781bb5c09f9de2fbbcace9e72297ea72',
        4: 'https://weather.com/tr-TR/weather/tenday/l/da66792fea4087022f72bc3219c55fd43aa018aec71006660d8eac450e038b7d',
        5: 'https://weather.com/tr-TR/weather/tenday/l/a41649a8c39ddefe33e31c77553d8015b4514b4bc8ece65a84c3e4e9914ccb2e',
        6: 'https://weather.com/tr-TR/weather/tenday/l/446a1ec141cc09780b30988572be95bea04c2509f14348db2df9142c0838a63e',
        7: 'https://weather.com/tr-TR/weather/tenday/l/980a69a73cc9e4029a2b7d7d3e14468ee44f1f266a706a7e328bb1f9d0b3f94e',
        8: 'https://weather.com/tr-TR/weather/tenday/l/385bcaeb40d32e52b385b4264071a7be79d7746852b379a330e2b045d34c12d7',
        9: 'https://weather.com/tr-TR/weather/tenday/l/323c91962adc622d57cf92f7dc81dd465b7e4a2b6de075ac31af63aa7fa8b8d7',
        10: 'https://weather.com/tr-TR/weather/tenday/l/1a096191b7d43fd9c1d62441dc135d51414d77c214d149754bd2abaaa6cb8d89',
        11: 'https://weather.com/tr-TR/weather/tenday/l/fcfd26f4e408b14d03d7365ec81f111ef6b4a3b7c82f6e799ef21e892a1c1f9e',
        12: 'https://weather.com/tr-TR/weather/tenday/l/ab7f13860f826fed825d0a08b79bc44eefbdb87373e183f4ba22c29beabab2a7',
        13: 'https://weather.com/tr-TR/weather/tenday/l/6674dd4fe53c3921597f2b04a1e95d0aa9562a7f760e50151b78490741a5d9ec',
        14: 'https://weather.com/tr-TR/weather/tenday/l/9a97cc3bf714b65f5dd839bb0cb8440de69aee37d4258f2babf1d0e368b0f860',
        15: 'https://weather.com/tr-TR/weather/tenday/l/d2a175f6e3bf2037558edf30dd6e2931b833af48af86d923e8b4eed747241f24',
        16: 'https://weather.com/tr-TR/weather/tenday/l/e0580ba52a7eb7d96cee65c68a024f1665ea72c22251167d7846437a767402ba',
        17: 'https://weather.com/tr-TR/weather/tenday/l/3e1c1be921457766ddc7f3031bf8e510ef398cef35026f2383195cc689e3c593',
        18: 'https://weather.com/tr-TR/weather/tenday/l/dd706b21b2f96648e5249d25c630d1e4ed39dd4f6e7d65eeb3d129ee944fb8e0',
        19: 'https://weather.com/tr-TR/weather/tenday/l/845648701dfa19e93e347238a10898b475e5a2a07d598863ed6b42366b4ecd94',
        20: 'https://weather.com/tr-TR/weather/tenday/l/b275f63264da052a907152fc7a94271fc7774f28baf5ca3b13952e676d50ea7b',
        21: 'https://weather.com/tr-TR/weather/tenday/l/3df6e899c36fa788b88ebc0397469b189ad43a1f56c0c41f45bfb6301f4a0d13',
        22: 'https://weather.com/tr-TR/weather/tenday/l/72819694ab5add8dba2e8bf0d1bea73507436fd778ba46896261c6daf7673207',
        23: 'https://weather.com/tr-TR/weather/tenday/l/530149dad37c3b944da43e5e142a61da951c35cf86d6db6d062402ee4860b4dc',
        24: 'https://weather.com/tr-TR/weather/tenday/l/5ef5f0bdd9b4b14a75977f5128a18eaa02b7a316ca87ad01d13cbcdcbc3ccea2',
        25: 'https://weather.com/tr-TR/weather/tenday/l/cbece3d75b0cb9bbdb3675e9782caadf3e4140358e1ce6e3f42cde6035b23aad',
        26: 'https://weather.com/tr-TR/weather/tenday/l/5a0641faf0bda7dbfc85746530f0b0211a9a4b122cfd345c6d4b619a8b3b35d3',
        27: 'https://weather.com/tr-TR/weather/tenday/l/054a587bd4c7b99b5ed929073c1e8edceefb3a4a9ab0768a4baf87c7bb53e510',
        28: 'https://weather.com/tr-TR/weather/tenday/l/22533930404db691cd07e6e74dd1c8850a9f1f87ec6d85dc2963363bf92ebdd7',
        29: 'https://weather.com/tr-TR/weather/tenday/l/bc52bd67dec30e3fa955bd1e67348e3213f3dbd55f5d47e4873aa0be647518db',
        30: 'https://weather.com/tr-TR/weather/tenday/l/c9813c2db8a277c6dc73d40325947bb501ec301fa79be7a30893fd56b43ea2c8',
        31: 'https://weather.com/tr-TR/weather/tenday/l/5743e401ba5dfc7d854de6a33554f30e34e24558cd2843f3fe58676fccb6b6a4',
        32: 'https://weather.com/tr-TR/weather/tenday/l/a1f355650324ab73fccf2a8384bf4f860dfc13d45b423e8d03d511cee4ac6660',
        33: 'https://weather.com/tr-TR/weather/tenday/l/0fc169ba768acf4d3087eeac08ca7d9933eb1b7073667b40c06d2b20ad5b531c',
        34: 'https://weather.com/tr-TR/weather/tenday/l/7912d03017522301f5c89f4f1d661d18ad10926c15063cf520ee5ec7ce7c787c',
        35: 'https://weather.com/tr-TR/weather/tenday/l/4484a5b53638342563a27f29638535026f50453ad8bf4c39afa9ec65676e215e',
        36: 'https://weather.com/tr-TR/weather/tenday/l/00d0e10741f35e3af2ae04569a396f47bd383b2ba29c73f6d860d5c754833e73',
        37: 'https://weather.com/tr-TR/weather/tenday/l/4883342af73ba85350d1b34e3cc1f574b183881e46a861d5738db107778ca9c0',
        38: 'https://weather.com/tr-TR/weather/tenday/l/c5d92539387edf61f80939e414a901314945a74bd026f65443502c3b5a13bb72',
        39: 'https://weather.com/tr-TR/weather/tenday/l/d83379f0c5034b63be66e81c93324fb9aeeadacbad5dd5da2b960d23724d7f9e',
        40: 'https://weather.com/tr-TR/weather/tenday/l/5c3041a0b6569e97e97493e4a3b78d20744b95518a7e416f7dc3b755286f8ab9',
        41: 'https://weather.com/tr-TR/weather/tenday/l/60e0035aa6ecf0156ebd855e899795c3c3677f9531d98f2b52e21fa260423c52',
        42: 'https://weather.com/tr-TR/weather/tenday/l/73da9c43b5d7a7592c49c955cddfdc0bc88defde7e21562e0d8d535f34a6a452',
        43: 'https://weather.com/tr-TR/weather/tenday/l/cd4d0d8563a569ea2093e490dc75069409cbb60e6d145a657e64222d8a749113',
        44: 'https://weather.com/tr-TR/weather/tenday/l/6a4c6f88ba0b2c1ca8cd6c595cc389899122bd4f06985f2eba8174ee8da08aa2',
        45: 'https://weather.com/tr-TR/weather/tenday/l/ff9c06e117f9b48ec9e2dca9fc1d9c46b87a0eccbea4a29b5e96bb8255e4f548',
        46: 'https://weather.com/tr-TR/weather/tenday/l/952368e9b686fc5ec21ebd20334d4b85d5d6cb0b1018fd5cb74bfa91f7e685a0',
        47: 'https://weather.com/tr-TR/weather/tenday/l/ab599c6598fb3436c96236fd130160736627b271caf6c5c8ec889eead1cc9b47',
        48: 'https://weather.com/tr-TR/weather/tenday/l/c8fbacdf7dedbd4ebe56574f1bd6cf39086ac1fbc418535ad57567bd21a98a33',
        49: 'https://weather.com/tr-TR/weather/tenday/l/f4ec83d153b94f8697abfdbf07a2b5c580fa06c026acaef53c322c4038d66274',
        50: 'https://weather.com/tr-TR/weather/tenday/l/fd12c5b98508b729be78883eda407956015efd59c8aac762f8645afc729ccbbc',
        51: 'https://weather.com/tr-TR/weather/tenday/l/b5f9b0a04b19eed2545350070e96b6113eb352c35204781f0361e5b4cba389f8',
        52: 'https://weather.com/tr-TR/weather/tenday/l/b791d013989c9c39907b8b9ff2ac8324f38036c112738a2a82a223c2fc8a766a',
        53: 'https://weather.com/tr-TR/weather/tenday/l/287978bf7ec866f46191666ae438cd0008a2cc6bb48b6a54a116fe5cb6e8cac6',
        54: 'https://weather.com/tr-TR/weather/tenday/l/22db5c656ecc9060ed7eb5a5723fc071ae30e988b4164f1a536b85564aee063c',
        55: 'https://weather.com/tr-TR/weather/tenday/l/86aac86877921d3415f227b9934d737b22ee38f818d4586466e584719801bac6',
        56: 'https://weather.com/tr-TR/weather/tenday/l/1cb5efc179b8ae4acd74620071b73a26f9870464820794461f6a9754faf86201',
        57: 'https://weather.com/tr-TR/weather/tenday/l/f5b86fe68f9fcd75417fff4dbc85a0f573e497c098b12a0a25e6f38e603d29a0',
        58: 'https://weather.com/tr-TR/weather/tenday/l/6164bd593b6fbb13ddb37e488761f4b9382c7d8731bd0f2f76fd7ded84f830d9',
        59: 'https://weather.com/tr-TR/weather/tenday/l/a145c318a9c1dbfd276620e1e1affb2532571da5ec0dbd64a1d6969690ecb8a2',
        60: 'https://weather.com/tr-TR/weather/tenday/l/82d41ec59953f2145b379720a3cd85a338369f35239b3e1fbfd7be680d5e9ce3',
        61: 'https://weather.com/tr-TR/weather/tenday/l/4e168acffa75110860f9bbea547cfc26a9db592b321d7bdbfcffcac951c5c801',
        62: 'https://weather.com/tr-TR/weather/tenday/l/7cf2b5d11d4e5ab4bb199a314b4ee26782147a3b9b4c477c8683323adebe77a6',
        63: 'https://weather.com/tr-TR/weather/tenday/l/044e9c5e6841335183a10e07d7b575c8dd7e52c0ba4d06b1278962d87fd5e14d',
        64: 'https://weather.com/tr-TR/weather/tenday/l/a425ac98bffc74046990375301656ba953ac5b99ca88312a26e5be602c2cb3ae',
        65: 'https://weather.com/tr-TR/weather/tenday/l/0eebfdec226fabf4e6e56dd4abb642174b72b35b8896b9d539a7de88e34d6a88',
        66: 'https://weather.com/tr-TR/weather/tenday/l/a86b9135e5fb2e57a988c843feb5e6de8a0df95cbb775c3cb5216b1d9d1e8236',
        67: 'https://weather.com/tr-TR/weather/tenday/l/82d47e276c969d5cae66b7013461cd53d27605919a7f2bda7d5a10ed90edf72f',
        68: 'https://weather.com/tr-TR/weather/tenday/l/418641c41d8ef34caf084498259f1c334226fcc49b44f198e49437634f564143',
        69: 'https://weather.com/tr-TR/weather/tenday/l/18550f473f54c7c5746d284d10a4a3aa952ca2fc691c1d7c6fe45788c379abca',
        70: 'https://weather.com/tr-TR/weather/tenday/l/357098e151c142dc10a4df960b12a3d223b1b4a4463cb1ff701d3914aadb4798',
        71: 'https://weather.com/tr-TR/weather/tenday/l/518cfe7cc6f3551fe0a7a4131557a4f743f69d856373095245a0f473a1efab29',
        72: 'https://weather.com/tr-TR/weather/tenday/l/e8dd08d675734ec2c0c0ac2403c375279c3ee3a6623cf4f2c8aef9cd70c7e63f',
        73: 'https://weather.com/tr-TR/weather/tenday/l/1afcafae08d41c59c6282a9c0b74caae2e35cf4ce4184d433380dc7fdf83e414',
        74: 'https://weather.com/tr-TR/weather/tenday/l/c3ec0230c701072f0c41f063b5985129e6fe8d177b6803f321a70654b35c8921',
        75: 'https://weather.com/tr-TR/weather/tenday/l/23571552e6b56a348afa5e7c1f9da1fe3e190d898fdc1c546647ee38c5cdf919',
        76: 'https://weather.com/tr-TR/weather/tenday/l/76182fc700e83797241171a53937db6c4829396674486b3ba1d98dfa1aaa7004',
        77: 'https://weather.com/tr-TR/weather/tenday/l/0cf9af64e681dc7d06d526b70ece09b7b687813e1b1b3d1fc671ea691389fd11',
        78: 'https://weather.com/tr-TR/weather/tenday/l/12629923f6caa3ad6966894caf57ec44865bb51eb1416c4eead8fe00bc02d1f3',
        79: 'https://weather.com/tr-TR/weather/tenday/l/3312af9db17b889f2520e57a2380ec2b52308bf1b945c77a2cd4ae3753447161',
        80: 'https://weather.com/tr-TR/weather/tenday/l/ef4fecfe688ea9541fd98af8b1907171b8dfdd319495e39949d92f4e30f0c502',
        81: 'https://weather.com/tr-TR/weather/tenday/l/1d44b5dcf873826a0e935a9c058ddb8e315e34b853f7a4c0e540fd2107d01089'
    }
    #Provincial home page links
    provincial_plate_mainPage = {
        1: 'https://weather.com/tr-TR/weather/today/l/759de7bce739bffeb0afb067e2292689c5e5c639ab58fee51064105554d9e294',
        2: 'https://weather.com/tr-TR/weather/today/l/e840d5313628355d0b0fcdffc4cefb5e21d6574cb44be670d7a3c5c4c6ca34fc',
        3: 'https://weather.com/tr-TR/weather/today/l/6915a0e957b64d10795353b30fca3378781bb5c09f9de2fbbcace9e72297ea72',
        4: 'https://weather.com/tr-TR/weather/today/l/da66792fea4087022f72bc3219c55fd43aa018aec71006660d8eac450e038b7d',
        5: 'https://weather.com/tr-TR/weather/today/l/a41649a8c39ddefe33e31c77553d8015b4514b4bc8ece65a84c3e4e9914ccb2e',
        6: 'https://weather.com/tr-TR/weather/today/l/446a1ec141cc09780b30988572be95bea04c2509f14348db2df9142c0838a63e',
        7: 'https://weather.com/tr-TR/weather/today/l/980a69a73cc9e4029a2b7d7d3e14468ee44f1f266a706a7e328bb1f9d0b3f94e',
        8: 'https://weather.com/tr-TR/weather/today/l/385bcaeb40d32e52b385b4264071a7be79d7746852b379a330e2b045d34c12d7',
        9: 'https://weather.com/tr-TR/weather/today/l/323c91962adc622d57cf92f7dc81dd465b7e4a2b6de075ac31af63aa7fa8b8d7',
        10: 'https://weather.com/tr-TR/weather/today/l/1a096191b7d43fd9c1d62441dc135d51414d77c214d149754bd2abaaa6cb8d89',
        11: 'https://weather.com/tr-TR/weather/today/l/fcfd26f4e408b14d03d7365ec81f111ef6b4a3b7c82f6e799ef21e892a1c1f9e',
        12: 'https://weather.com/tr-TR/weather/today/l/ab7f13860f826fed825d0a08b79bc44eefbdb87373e183f4ba22c29beabab2a7',
        13: 'https://weather.com/tr-TR/weather/today/l/6674dd4fe53c3921597f2b04a1e95d0aa9562a7f760e50151b78490741a5d9ec',
        14: 'https://weather.com/tr-TR/weather/today/l/9a97cc3bf714b65f5dd839bb0cb8440de69aee37d4258f2babf1d0e368b0f860',
        15: 'https://weather.com/tr-TR/weather/today/l/d2a175f6e3bf2037558edf30dd6e2931b833af48af86d923e8b4eed747241f24',
        16: 'https://weather.com/tr-TR/weather/today/l/e0580ba52a7eb7d96cee65c68a024f1665ea72c22251167d7846437a767402ba',
        17: 'https://weather.com/tr-TR/weather/today/l/3e1c1be921457766ddc7f3031bf8e510ef398cef35026f2383195cc689e3c593',
        18: 'https://weather.com/tr-TR/weather/today/l/dd706b21b2f96648e5249d25c630d1e4ed39dd4f6e7d65eeb3d129ee944fb8e0',
        19: 'https://weather.com/tr-TR/weather/today/l/845648701dfa19e93e347238a10898b475e5a2a07d598863ed6b42366b4ecd94',
        20: 'https://weather.com/tr-TR/weather/today/l/b275f63264da052a907152fc7a94271fc7774f28baf5ca3b13952e676d50ea7b',
        21: 'https://weather.com/tr-TR/weather/today/l/3df6e899c36fa788b88ebc0397469b189ad43a1f56c0c41f45bfb6301f4a0d13',
        22: 'https://weather.com/tr-TR/weather/today/l/72819694ab5add8dba2e8bf0d1bea73507436fd778ba46896261c6daf7673207',
        23: 'https://weather.com/tr-TR/weather/today/l/530149dad37c3b944da43e5e142a61da951c35cf86d6db6d062402ee4860b4dc',
        24: 'https://weather.com/tr-TR/weather/today/l/5ef5f0bdd9b4b14a75977f5128a18eaa02b7a316ca87ad01d13cbcdcbc3ccea2',
        25: 'https://weather.com/tr-TR/weather/today/l/cbece3d75b0cb9bbdb3675e9782caadf3e4140358e1ce6e3f42cde6035b23aad',
        26: 'https://weather.com/tr-TR/weather/today/l/5a0641faf0bda7dbfc85746530f0b0211a9a4b122cfd345c6d4b619a8b3b35d3',
        27: 'https://weather.com/tr-TR/weather/today/l/054a587bd4c7b99b5ed929073c1e8edceefb3a4a9ab0768a4baf87c7bb53e510',
        28: 'https://weather.com/tr-TR/weather/today/l/22533930404db691cd07e6e74dd1c8850a9f1f87ec6d85dc2963363bf92ebdd7',
        29: 'https://weather.com/tr-TR/weather/today/l/bc52bd67dec30e3fa955bd1e67348e3213f3dbd55f5d47e4873aa0be647518db',
        30: 'https://weather.com/tr-TR/weather/today/l/c9813c2db8a277c6dc73d40325947bb501ec301fa79be7a30893fd56b43ea2c8',
        31: 'https://weather.com/tr-TR/weather/today/l/5743e401ba5dfc7d854de6a33554f30e34e24558cd2843f3fe58676fccb6b6a4',
        32: 'https://weather.com/tr-TR/weather/today/l/a1f355650324ab73fccf2a8384bf4f860dfc13d45b423e8d03d511cee4ac6660',
        33: 'https://weather.com/tr-TR/weather/today/l/0fc169ba768acf4d3087eeac08ca7d9933eb1b7073667b40c06d2b20ad5b531c',
        34: 'https://weather.com/tr-TR/weather/today/l/7912d03017522301f5c89f4f1d661d18ad10926c15063cf520ee5ec7ce7c787c',
        35: 'https://weather.com/tr-TR/weather/today/l/4484a5b53638342563a27f29638535026f50453ad8bf4c39afa9ec65676e215e',
        36: 'https://weather.com/tr-TR/weather/today/l/00d0e10741f35e3af2ae04569a396f47bd383b2ba29c73f6d860d5c754833e73',
        37: 'https://weather.com/tr-TR/weather/today/l/4883342af73ba85350d1b34e3cc1f574b183881e46a861d5738db107778ca9c0',
        38: 'https://weather.com/tr-TR/weather/today/l/c5d92539387edf61f80939e414a901314945a74bd026f65443502c3b5a13bb72',
        39: 'https://weather.com/tr-TR/weather/today/l/d83379f0c5034b63be66e81c93324fb9aeeadacbad5dd5da2b960d23724d7f9e',
        40: 'https://weather.com/tr-TR/weather/today/l/5c3041a0b6569e97e97493e4a3b78d20744b95518a7e416f7dc3b755286f8ab9',
        41: 'https://weather.com/tr-TR/weather/today/l/60e0035aa6ecf0156ebd855e899795c3c3677f9531d98f2b52e21fa260423c52',
        42: 'https://weather.com/tr-TR/weather/today/l/73da9c43b5d7a7592c49c955cddfdc0bc88defde7e21562e0d8d535f34a6a452',
        43: 'https://weather.com/tr-TR/weather/today/l/cd4d0d8563a569ea2093e490dc75069409cbb60e6d145a657e64222d8a749113',
        44: 'https://weather.com/tr-TR/weather/today/l/6a4c6f88ba0b2c1ca8cd6c595cc389899122bd4f06985f2eba8174ee8da08aa2',
        45: 'https://weather.com/tr-TR/weather/today/l/ff9c06e117f9b48ec9e2dca9fc1d9c46b87a0eccbea4a29b5e96bb8255e4f548',
        46: 'https://weather.com/tr-TR/weather/today/l/952368e9b686fc5ec21ebd20334d4b85d5d6cb0b1018fd5cb74bfa91f7e685a0',
        47: 'https://weather.com/tr-TR/weather/today/l/ab599c6598fb3436c96236fd130160736627b271caf6c5c8ec889eead1cc9b47',
        48: 'https://weather.com/tr-TR/weather/today/l/c8fbacdf7dedbd4ebe56574f1bd6cf39086ac1fbc418535ad57567bd21a98a33',
        49: 'https://weather.com/tr-TR/weather/today/l/f4ec83d153b94f8697abfdbf07a2b5c580fa06c026acaef53c322c4038d66274',
        50: 'https://weather.com/tr-TR/weather/today/l/fd12c5b98508b729be78883eda407956015efd59c8aac762f8645afc729ccbbc',
        51: 'https://weather.com/tr-TR/weather/today/l/b5f9b0a04b19eed2545350070e96b6113eb352c35204781f0361e5b4cba389f8',
        52: 'https://weather.com/tr-TR/weather/today/l/b791d013989c9c39907b8b9ff2ac8324f38036c112738a2a82a223c2fc8a766a',
        53: 'https://weather.com/tr-TR/weather/today/l/287978bf7ec866f46191666ae438cd0008a2cc6bb48b6a54a116fe5cb6e8cac6',
        54: 'https://weather.com/tr-TR/weather/today/l/22db5c656ecc9060ed7eb5a5723fc071ae30e988b4164f1a536b85564aee063c',
        55: 'https://weather.com/tr-TR/weather/today/l/86aac86877921d3415f227b9934d737b22ee38f818d4586466e584719801bac6',
        56: 'https://weather.com/tr-TR/weather/today/l/1cb5efc179b8ae4acd74620071b73a26f9870464820794461f6a9754faf86201',
        57: 'https://weather.com/tr-TR/weather/today/l/f5b86fe68f9fcd75417fff4dbc85a0f573e497c098b12a0a25e6f38e603d29a0',
        58: 'https://weather.com/tr-TR/weather/today/l/6164bd593b6fbb13ddb37e488761f4b9382c7d8731bd0f2f76fd7ded84f830d9',
        59: 'https://weather.com/tr-TR/weather/today/l/a145c318a9c1dbfd276620e1e1affb2532571da5ec0dbd64a1d6969690ecb8a2',
        60: 'https://weather.com/tr-TR/weather/today/l/82d41ec59953f2145b379720a3cd85a338369f35239b3e1fbfd7be680d5e9ce3',
        61: 'https://weather.com/tr-TR/weather/today/l/4e168acffa75110860f9bbea547cfc26a9db592b321d7bdbfcffcac951c5c801',
        62: 'https://weather.com/tr-TR/weather/today/l/7cf2b5d11d4e5ab4bb199a314b4ee26782147a3b9b4c477c8683323adebe77a6',
        63: 'https://weather.com/tr-TR/weather/today/l/044e9c5e6841335183a10e07d7b575c8dd7e52c0ba4d06b1278962d87fd5e14d',
        64: 'https://weather.com/tr-TR/weather/today/l/a425ac98bffc74046990375301656ba953ac5b99ca88312a26e5be602c2cb3ae',
        65: 'https://weather.com/tr-TR/weather/today/l/0eebfdec226fabf4e6e56dd4abb642174b72b35b8896b9d539a7de88e34d6a88',
        66: 'https://weather.com/tr-TR/weather/today/l/a86b9135e5fb2e57a988c843feb5e6de8a0df95cbb775c3cb5216b1d9d1e8236',
        67: 'https://weather.com/tr-TR/weather/today/l/82d47e276c969d5cae66b7013461cd53d27605919a7f2bda7d5a10ed90edf72f',
        68: 'https://weather.com/tr-TR/weather/today/l/418641c41d8ef34caf084498259f1c334226fcc49b44f198e49437634f564143',
        69: 'https://weather.com/tr-TR/weather/today/l/18550f473f54c7c5746d284d10a4a3aa952ca2fc691c1d7c6fe45788c379abca',
        70: 'https://weather.com/tr-TR/weather/today/l/357098e151c142dc10a4df960b12a3d223b1b4a4463cb1ff701d3914aadb4798',
        71: 'https://weather.com/tr-TR/weather/today/l/518cfe7cc6f3551fe0a7a4131557a4f743f69d856373095245a0f473a1efab29',
        72: 'https://weather.com/tr-TR/weather/today/l/e8dd08d675734ec2c0c0ac2403c375279c3ee3a6623cf4f2c8aef9cd70c7e63f',
        73: 'https://weather.com/tr-TR/weather/today/l/1afcafae08d41c59c6282a9c0b74caae2e35cf4ce4184d433380dc7fdf83e414',
        74: 'https://weather.com/tr-TR/weather/today/l/c3ec0230c701072f0c41f063b5985129e6fe8d177b6803f321a70654b35c8921',
        75: 'https://weather.com/tr-TR/weather/today/l/79c880f34f6d3c9284f27a994c9d7a8bbc3ebb7a58a65fb2d2bf50a6202167f1',
        76: 'https://weather.com/tr-TR/weather/today/l/76182fc700e83797241171a53937db6c4829396674486b3ba1d98dfa1aaa7004',
        77: 'https://weather.com/tr-TR/weather/today/l/0cf9af64e681dc7d06d526b70ece09b7b687813e1b1b3d1fc671ea691389fd11',
        78: 'https://weather.com/tr-TR/weather/today/l/12629923f6caa3ad6966894caf57ec44865bb51eb1416c4eead8fe00bc02d1f3',
        79: 'https://weather.com/tr-TR/weather/today/l/3312af9db17b889f2520e57a2380ec2b52308bf1b945c77a2cd4ae3753447161',
        80: 'https://weather.com/tr-TR/weather/today/l/ef4fecfe688ea9541fd98af8b1907171b8dfdd319495e39949d92f4e30f0c502',
        81: 'https://weather.com/tr-TR/weather/today/l/1d44b5dcf873826a0e935a9c058ddb8e315e34b853f7a4c0e540fd2107d01089'
    }

    def start_requests(self):
        # Initialize lists to store URLs
        final_urls = []
        today_urls = []
        # Populate URL lists
        for i in range(1, 82):
            url = self.provincial_plate[i]
            url2 = self.provincial_plate_mainPage[i]
            final_urls.append(url)
            today_urls.append(url2)

        # Generate requests for final URLs
        counter = 0
        for url in final_urls:
            counter = counter + 1
            # Send a request for each final URL, with plate_codes as a metadata
            yield scrapy.Request(url=url, callback=self.parse, meta={'plate_codes': counter})

        counter = 0
        for url in today_urls:
            counter = counter + 1
            # Send a request for each final URL, with plate_codes as a metadata
            yield scrapy.Request(url=url, callback=self.parse, meta={'plate_codes': counter})

    def parse(self, response):
        # Get the current date and time
        current_date = datetime.datetime.now()
        # Extract objects from the response
        objects = response.xpath(self.ıbm_json["ıbm_objects"])
        # Create a WeatherCrawlerItem instance
        item = WeatherCrawlerItem()
        # Check if no objects are found
        if not objects:
            # Set item fields for default values
            item['date'] = current_date.strftime('%Y-%m-%d')
            item['up'] = response.xpath(self.ıbm_json["ıbm_up"]).get()
            item['low'] = response.xpath(self.ıbm_json["ıbm_low"]).get()
            item['plate_codes'] = response.meta.get('plate_codes')
            print(item)
            yield item
        # Iterate over a subset of objects
        for object in objects[1:7]:
            # Extract the day from the date string using a regular expression
            day = re.search(self.ıbm_json["ıbm_delete_pattern"], object.xpath(self.ıbm_json["ıbm_date"]).get()).group(1)
            # Set the item fields with the extracted information
            item['date'] = datetime.datetime(year=2023, month=11, day=int(day)).strftime('%Y-%m-%d')
            item['up'] = object.xpath(self.ıbm_json["ıbm_up"]).get()
            item['low'] = object.xpath(self.ıbm_json["ıbm_low"]).get()
            item['plate_codes'] = response.meta.get('plate_codes')
            yield item



