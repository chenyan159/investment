# Research runner 2026-06-20 运行结果审计

审计时间：2026-06-21T02:00:09.479Z

## 总结

- 本轮 done 任务：47（公司调研 22，公司评估 22，会议 file-run 3）。
- 输出文件存在：47/47；runner post-run verification 通过：47/47。
- 结构质量：PASS 47，REVIEW 0，FAIL 0。
- 旧版备份：44 项有备份且文件存在；3 项无备份（均为新增会议 file-run）；备份缺失 0。
- 与旧版大小对比：24 项更大或持平，20 项更短。
- 重试后成功：NVDA(2), MSFT(2), AMD(2)。

## 质量结论

- 47 个输出全部存在，全部有 runner post-run verification passed。
- 未发现空文件、缺一级标题、明显占位符/TODO、输出到错误目录、备份缺失，或评估报告把目标价/投资评级当作经营传导证据的问题。
- 4 个公司调研文件在第一轮关键词检查中被误报为缺“五季财报”，复核后均存在相应表格：MSFT、MRVL、EQIX、JBL。
- 会议 file-run 三项是新增文件，runner 未记录旧版 from/to，因此没有旧版备份；目录中也只看到本轮 `2026-06-20` 的 conference_update 文件。

## 较旧版明显缩短但结构通过的文件

- company/TSEM: -6526 bytes，12 行；结构检查通过，建议人工阅读重点关注是否有旧版细节被压缩。输出：公司调研/晶圆制造_前道设备/TSEM_Tower Semiconductor_公司调研_2026-06-20.md
- company/EQIX: -5439 bytes，21 行；结构检查通过，建议人工阅读重点关注是否有旧版细节被压缩。输出：公司调研/云算力_IDC_AI软件平台/EQIX_Equinix_公司调研_2026-06-20.md
- company/ORCL: -7043 bytes，-153 行；结构检查通过，建议人工阅读重点关注是否有旧版细节被压缩。输出：公司调研/云算力_IDC_AI软件平台/ORCL_Oracle Corporation_公司调研_2026-06-20.md
- company-evaluation/NVDA: -8901 bytes，3 行；结构检查通过，建议人工阅读重点关注是否有旧版细节被压缩。输出：分析报告/公司评估/NVDA_NVIDIA_收入传导估值评估_2026-06-20.md
- company-evaluation/VRT: -6288 bytes，-3 行；结构检查通过，建议人工阅读重点关注是否有旧版细节被压缩。输出：分析报告/公司评估/VRT_Vertiv_收入传导估值评估_2026-06-20.md
- company-evaluation/CSCO: -8365 bytes，-9 行；结构检查通过，建议人工阅读重点关注是否有旧版细节被压缩。输出：分析报告/公司评估/CSCO_Cisco_Systems_收入传导估值评估_2026-06-20.md

## 47 个任务明细

| # | 类型 | 标的 | 输出路径 | 质量 | 当前大小/行数 | 旧版备份 | 对比旧版 | attempts |
|---:|---|---|---|---|---:|---|---|---:|
| 1 | company | AMZN | 公司调研/云算力_IDC_AI软件平台/AMZN_Amazon_公司调研_2026-06-20.md | PASS | 44.7 KB / 433 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/AMZN_2026-06-20T12_37_58-07_00-48b1f0ef25/AMZN_Amazon_公司调研_2026-06-11.md | +5248 bytes; +20 行; URL -5 | 1 |
| 2 | company | GOOGL | 公司调研/云算力_IDC_AI软件平台/GOOGL_Alphabet Inc_公司调研_2026-06-20.md | PASS | 49.7 KB / 445 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/GOOGL_2026-06-20T12_37_58-07_00-48b1f0ef25/GOOGL_Alphabet_Inc_公司调研_2026-06-12.md | +2605 bytes; -2 行; URL -1 | 1 |
| 3 | company | NVDA | 公司调研/AI计算芯片_EDA_IP_custom_ASIC/NVDA_NVIDIA_公司调研_2026-06-20.md | PASS | 47.8 KB / 424 | 已备份：公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/NVDA_2026-06-20T12_41_42-07_00-61dfac234e/NVDA_NVIDIA_公司调研_2026-06-11.md | +5569 bytes; +16 行; URL -6 | 2 |
| 4 | company | MSFT | 公司调研/云算力_IDC_AI软件平台/MSFT_微软_公司调研_2026-06-20.md | PASS | 48.7 KB / 443 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/MSFT_2026-06-20T12_43_24-07_00-28f17e3b62/MSFT_微软_公司调研_2026-06-12.md | +445 bytes; +43 行; URL -8 | 2 |
| 5 | company | COHR | 公司调研/AI网络_光互联_连接器/COHR_Coherent_公司调研_2026-06-20.md | PASS | 45.7 KB / 484 | 已备份：公司调研/AI网络_光互联_连接器/备份/COHR_2026-06-20T12_52_39-07_00-770c995606/COHR_Coherent_公司调研_2026-06-11.md | -299 bytes; +79 行; URL +1 | 1 |
| 6 | company | META | 公司调研/云算力_IDC_AI软件平台/META_Meta Platforms_公司调研_2026-06-20.md | PASS | 55.0 KB / 603 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/META_2026-06-20T12_51_40-07_00-47558d3459/META_Meta Platforms_公司调研_2026-06-11.md | +18403 bytes; +204 行; URL -4 | 1 |
| 7 | company | HPE | 公司调研/AI服务器_存储_EMS/HPE_惠普企业_公司调研_2026-06-20.md | PASS | 51.9 KB / 436 | 已备份：公司调研/AI服务器_存储_EMS/备份/HPE_2026-06-20T12_58_17-07_00-6f01479642/HPE_惠普企业_公司调研_2026-06-11.md | +5224 bytes; +11 行; URL -5 | 1 |
| 8 | company | MRVL | 公司调研/AI计算芯片_EDA_IP_custom_ASIC/MRVL_Marvell Technology_公司调研_2026-06-20.md | PASS | 54.4 KB / 442 | 已备份：公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/MRVL_2026-06-20T12_59_40-07_00-9faa3bc0bc/MRVL_Marvell Technology_公司调研_2026-06-11.md | +6492 bytes; +56 行; URL +1 | 1 |
| 9 | company | TSEM | 公司调研/晶圆制造_前道设备/TSEM_Tower Semiconductor_公司调研_2026-06-20.md | PASS | 40.0 KB / 417 | 已备份：公司调研/晶圆制造_前道设备/备份/TSEM_2026-06-20T13_09_45-07_00-395fbf3b09/TSEM_Tower Semiconductor_公司调研_2026-06-11.md | -6526 bytes; +12 行; URL +2 | 1 |
| 10 | company | AMD | 公司调研/AI计算芯片_EDA_IP_custom_ASIC/AMD_Advanced Micro Devices_公司调研_2026-06-20.md | PASS | 42.7 KB / 329 | 已备份：公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/AMD_2026-06-20T13_14_22-07_00-b6f127e993/AMD_Advanced_Micro_Devices_公司调研_2026-06-11.md | -2301 bytes; -60 行; URL -5 | 2 |
| 11 | company | TSM | 公司调研/晶圆制造_前道设备/TSM_台积电_公司调研_2026-06-20.md | PASS | 43.2 KB / 382 | 已备份：公司调研/晶圆制造_前道设备/备份/TSM_2026-06-20T13_17_18-07_00-5b3df3a1f2/TSM_台积电_公司调研_2026-06-11.md | +1927 bytes; -10 行; URL -1 | 1 |
| 12 | company | BABA | 公司调研/云算力_IDC_AI软件平台/BABA_Alibaba阿里巴巴_公司调研_2026-06-20.md | PASS | 42.9 KB / 335 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/BABA_2026-06-20T13_18_48-07_00-f234500052/BABA_Alibaba 阿里巴巴_公司调研_2026-06-11.md | -138 bytes; +7 行; URL -3 | 1 |
| 13 | company | ETN | 公司调研/配电_电源_功率器件/ETN_Eaton Corporation_公司调研_2026-06-20.md | PASS | 43.8 KB / 364 | 已备份：公司调研/配电_电源_功率器件/备份/ETN_2026-06-20T13_29_21-07_00-2589ccd314/ETN_Eaton_Corporation_公司调研_2026-06-12.md | -4509 bytes; -3 行; URL -9 | 1 |
| 14 | company | EQIX | 公司调研/云算力_IDC_AI软件平台/EQIX_Equinix_公司调研_2026-06-20.md | PASS | 45.5 KB / 445 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/EQIX_2026-06-20T13_26_11-07_00-f31018d3ff/EQIX_Equinix_公司调研_2026-06-12.md | -5439 bytes; +21 行; URL -3 | 1 |
| 15 | company | VRT | 公司调研/机电_冷却_工程_水处理_边缘工业AI/VRT_Vertiv_公司调研_2026-06-20.md | PASS | 45.1 KB / 374 | 已备份：公司调研/机电_冷却_工程_水处理_边缘工业AI/备份/VRT_2026-06-20T13_30_18-07_00-1a2afb9d49/VRT_Vertiv_公司调研_2026-06-11.md | +1931 bytes; -17 行; URL -2 | 1 |
| 16 | company | AVGO | 公司调研/AI计算芯片_EDA_IP_custom_ASIC/AVGO_Broadcom_公司调研_2026-06-20.md | PASS | 44.3 KB / 422 | 已备份：公司调研/AI计算芯片_EDA_IP_custom_ASIC/备份/AVGO_2026-06-20T13_33_19-07_00-856c762a54/AVGO_Broadcom_公司调研_2026-06-11.md | -991 bytes; +62 行; URL +3 | 1 |
| 17 | company | CIEN | 公司调研/AI网络_光互联_连接器/CIEN_Ciena Corporation_公司调研_2026-06-20.md | PASS | 45.5 KB / 457 | 已备份：公司调研/AI网络_光互联_连接器/备份/CIEN_2026-06-20T13_44_32-07_00-081b965206/CIEN_Ciena_Corporation_公司调研_2026-06-11.md | +15 bytes; +16 行; URL +7 | 1 |
| 18 | company | CSCO | 公司调研/AI网络_光互联_连接器/CSCO_Cisco Systems_公司调研_2026-06-20.md | PASS | 52.7 KB / 509 | 已备份：公司调研/AI网络_光互联_连接器/备份/CSCO_2026-06-20T13_44_12-07_00-2fb065f222/CSCO_Cisco Systems_公司调研_2026-06-11.md | +8051 bytes; +115 行; URL -4 | 1 |
| 19 | company | ORCL | 公司调研/云算力_IDC_AI软件平台/ORCL_Oracle Corporation_公司调研_2026-06-20.md | PASS | 40.4 KB / 346 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/ORCL_2026-06-20T13_47_33-07_00-902e7b384e/ORCL_Oracle Corporation_公司调研_2026-06-12.md | -7043 bytes; -153 行; URL +3 | 1 |
| 20 | company | FCEL | 公司调研/电力_发电_能源_储能/FCEL_FuelCell_Energy_公司调研_2026-06-20.md | PASS | 43.6 KB / 396 | 已备份：公司调研/电力_发电_能源_储能/备份/FCEL_2026-06-20T13_46_09-07_00-c418c3c52d/FCEL_FuelCell Energy_公司调研_2026-06-11.md | +532 bytes; -15 行; URL -1 | 1 |
| 21 | company | ADBE | 公司调研/云算力_IDC_AI软件平台/ADBE_Adobe_公司调研_2026-06-20.md | PASS | 45.8 KB / 422 | 已备份：公司调研/云算力_IDC_AI软件平台/备份/ADBE_2026-06-20T13_55_09-07_00-54ae1e936b/ADBE_Adobe_公司调研_2026-06-11.md | +1822 bytes; +45 行; URL +0 | 1 |
| 22 | company | JBL | 公司调研/AI服务器_存储_EMS/JBL_Jabil Inc_公司调研_2026-06-20.md | PASS | 50.8 KB / 480 | 已备份：公司调研/AI服务器_存储_EMS/备份/JBL_2026-06-20T13_56_13-07_00-f32fe324a2/JBL_Jabil Inc_公司调研_2026-06-11.md | +996 bytes; +23 行; URL -8 | 1 |
| 23 | company-evaluation | MSFT | 分析报告/公司评估/MSFT_微软_收入传导估值评估_2026-06-20.md | PASS | 36.3 KB / 171 | 已备份：分析报告/公司评估/备份/MSFT_2026-06-20T14_10_00-07_00-965a569958/MSFT_微软_收入传导估值评估_2026-06-12.md | -3316 bytes; -28 行; URL +0 | 1 |
| 24 | company-evaluation | GOOGL | 分析报告/公司评估/GOOGL_Alphabet_Inc_收入传导估值评估_2026-06-20.md | PASS | 33.1 KB / 174 | 已备份：分析报告/公司评估/备份/GOOGL_2026-06-20T14_10_00-07_00-965a569958/GOOGL_Alphabet_Inc_收入传导估值评估_2026-06-12.md | -4652 bytes; -1 行; URL +3 | 1 |
| 25 | company-evaluation | NVDA | 分析报告/公司评估/NVDA_NVIDIA_收入传导估值评估_2026-06-20.md | PASS | 31.1 KB / 172 | 已备份：分析报告/公司评估/备份/NVDA_2026-06-20T14_10_00-07_00-965a569958/NVDA_NVIDIA_收入传导估值评估_2026-06-12.md | -8901 bytes; +3 行; URL -6 | 1 |
| 26 | company-evaluation | AMZN | 分析报告/公司评估/AMZN_Amazon_收入传导估值评估_2026-06-20.md | PASS | 35.5 KB / 184 | 已备份：分析报告/公司评估/备份/AMZN_2026-06-20T14_10_00-07_00-965a569958/AMZN_Amazon_收入传导估值评估_2026-06-12.md | +507 bytes; +17 行; URL -2 | 1 |
| 27 | company-evaluation | COHR | 分析报告/公司评估/COHR_Coherent_收入传导估值评估_2026-06-20.md | PASS | 39.4 KB / 204 | 已备份：分析报告/公司评估/备份/COHR_2026-06-20T14_19_20-07_00-0d88c6f5d4/COHR_Coherent_收入传导估值评估_2026-06-12.md | +5341 bytes; +33 行; URL +4 | 1 |
| 28 | company-evaluation | HPE | 分析报告/公司评估/HPE_惠普企业_收入传导估值评估_2026-06-20.md | PASS | 41.8 KB / 179 | 已备份：分析报告/公司评估/备份/HPE_2026-06-20T14_19_54-07_00-d52bdbeb90/HPE_惠普企业_收入传导估值评估_2026-06-12.md | +6434 bytes; +5 行; URL +1 | 1 |
| 29 | company-evaluation | META | 分析报告/公司评估/META_Meta_Platforms_收入传导估值评估_2026-06-20.md | PASS | 35.7 KB / 181 | 已备份：分析报告/公司评估/备份/META_2026-06-20T14_19_20-07_00-0d88c6f5d4/META_Meta_Platforms_收入传导估值评估_2026-06-12.md | +6388 bytes; +37 行; URL +1 | 1 |
| 30 | company-evaluation | MRVL | 分析报告/公司评估/MRVL_Marvell_Technology_收入传导估值评估_2026-06-20.md | PASS | 43.4 KB / 198 | 已备份：分析报告/公司评估/备份/MRVL_2026-06-20T14_20_13-07_00-2f0707c722/MRVL_Marvell_Technology_收入传导估值评估_2026-06-12.md | +4496 bytes; +20 行; URL +6 | 1 |
| 31 | company-evaluation | TSEM | 分析报告/公司评估/TSEM_Tower_Semiconductor_收入传导估值评估_2026-06-20.md | PASS | 33.5 KB / 144 | 已备份：分析报告/公司评估/备份/TSEM_2026-06-20T14_28_30-07_00-b73ffef6a5/TSEM_Tower_Semiconductor_收入传导估值评估_2026-06-12.md | +570 bytes; -12 行; URL -5 | 1 |
| 32 | company-evaluation | TSM | 分析报告/公司评估/TSM_台积电_收入传导估值评估_2026-06-20.md | PASS | 38.0 KB / 167 | 已备份：分析报告/公司评估/备份/TSM_2026-06-20T14_29_23-07_00-5fabc8441f/TSM_台积电_收入传导估值评估_2026-06-12.md | +2167 bytes; -1 行; URL +12 | 1 |
| 33 | company-evaluation | BABA | 分析报告/公司评估/BABA_Alibaba_阿里巴巴_收入传导估值评估_2026-06-20.md | PASS | 32.7 KB / 170 | 已备份：分析报告/公司评估/备份/BABA_2026-06-20T14_29_42-07_00-41caca48e2/BABA_Alibaba_阿里巴巴_收入传导估值评估_2026-06-12.md | -3328 bytes; +4 行; URL +2 | 1 |
| 34 | company-evaluation | AMD | 分析报告/公司评估/AMD_Advanced_Micro_Devices_收入传导估值评估_2026-06-20.md | PASS | 39.3 KB / 175 | 已备份：分析报告/公司评估/备份/AMD_2026-06-20T14_29_14-07_00-95f3d8f8a3/AMD_Advanced_Micro_Devices_收入传导估值评估_2026-06-12.md | -1132 bytes; -4 行; URL +1 | 1 |
| 35 | company-evaluation | EQIX | 分析报告/公司评估/EQIX_Equinix_收入传导估值评估_2026-06-20.md | PASS | 39.0 KB / 171 | 已备份：分析报告/公司评估/备份/EQIX_2026-06-20T14_36_17-07_00-a4fac0062c/EQIX_Equinix_收入传导估值评估_2026-06-12.md | +4940 bytes; +29 行; URL +3 | 1 |
| 36 | company-evaluation | ETN | 分析报告/公司评估/ETN_Eaton_Corporation_收入传导估值评估_2026-06-20.md | PASS | 42.9 KB / 194 | 已备份：分析报告/公司评估/备份/ETN_2026-06-20T14_38_10-07_00-73263d6224/ETN_Eaton_Corporation_收入传导估值评估_2026-06-12.md | -359 bytes; +26 行; URL +0 | 1 |
| 37 | company-evaluation | VRT | 分析报告/公司评估/VRT_Vertiv_收入传导估值评估_2026-06-20.md | PASS | 37.7 KB / 166 | 已备份：分析报告/公司评估/备份/VRT_2026-06-20T14_38_46-07_00-04e55286dc/VRT_Vertiv_收入传导估值评估_2026-06-12.md | -6288 bytes; -3 行; URL +3 | 1 |
| 38 | company-evaluation | CSCO | 分析报告/公司评估/CSCO_Cisco_Systems_收入传导估值评估_2026-06-20.md | PASS | 33.9 KB / 174 | 已备份：分析报告/公司评估/备份/CSCO_2026-06-20T14_44_22-07_00-a2a83c27b6/CSCO_Cisco_Systems_收入传导估值评估_2026-06-12.md | -8365 bytes; -9 行; URL +0 | 1 |
| 39 | company-evaluation | CIEN | 分析报告/公司评估/CIEN_Ciena_Corporation_收入传导估值评估_2026-06-20.md | PASS | 35.0 KB / 165 | 已备份：分析报告/公司评估/备份/CIEN_2026-06-20T14_48_49-07_00-61cdf71986/CIEN_Ciena_Corporation_收入传导估值评估_2026-06-12.md | +1100 bytes; +8 行; URL -4 | 1 |
| 40 | company-evaluation | FCEL | 分析报告/公司评估/FCEL_FuelCell_Energy_收入传导估值评估_2026-06-20.md | PASS | 32.7 KB / 166 | 已备份：分析报告/公司评估/备份/FCEL_2026-06-20T14_50_04-07_00-fa61490f07/FCEL_FuelCell_Energy_收入传导估值评估_2026-06-12.md | -1496 bytes; +9 行; URL -1 | 1 |
| 41 | company-evaluation | AVGO | 分析报告/公司评估/AVGO_Broadcom_收入传导估值评估_2026-06-20.md | PASS | 30.4 KB / 147 | 已备份：分析报告/公司评估/备份/AVGO_2026-06-20T14_43_33-07_00-6714f6a32f/AVGO_Broadcom_收入传导估值评估_2026-06-12.md | -4127 bytes; -22 行; URL +0 | 1 |
| 42 | company-evaluation | ORCL | 分析报告/公司评估/ORCL_Oracle_Corporation_收入传导估值评估_2026-06-20.md | PASS | 33.4 KB / 169 | 已备份：分析报告/公司评估/备份/ORCL_2026-06-20T14_51_58-07_00-5f604f5a13/ORCL_Oracle_Corporation_收入传导估值评估_2026-06-12.md | +1336 bytes; +18 行; URL -2 | 1 |
| 43 | company-evaluation | ADBE | 分析报告/公司评估/ADBE_Adobe_收入传导估值评估_2026-06-20.md | PASS | 40.2 KB / 178 | 已备份：分析报告/公司评估/备份/ADBE_2026-06-20T14_57_14-07_00-51d83b1036/ADBE_Adobe_收入传导估值评估_2026-06-12.md | -968 bytes; +2 行; URL +0 | 1 |
| 44 | company-evaluation | JBL | 分析报告/公司评估/JBL_Jabil_Inc_收入传导估值评估_2026-06-20.md | PASS | 36.0 KB / 159 | 已备份：分析报告/公司评估/备份/JBL_2026-06-20T14_58_13-07_00-23e3b6dea1/JBL_Jabil_Inc_收入传导估值评估_2026-06-12.md | -2510 bytes; -27 行; URL -2 | 1 |
| 45 | file-run | conference_oip_2026 | 行业调研/产业背景/顶级会议信息/conference_update_oip_2026_2026-06-20.md | PASS | 43.3 KB / 250 | 无旧版备份/新文件 | n/a | 1 |
| 46 | file-run | conference_hpe_discover_2026 | 行业调研/产业背景/顶级会议信息/conference_update_hpe_discover_2026_2026-06-20.md | PASS | 34.2 KB / 186 | 无旧版备份/新文件 | n/a | 1 |
| 47 | file-run | conference_ieee_vlsi_symposium_2026 | 行业调研/产业背景/顶级会议信息/conference_update_ieee_vlsi_symposium_2026_2026-06-20.md | PASS | 42.6 KB / 300 | 无旧版备份/新文件 | n/a | 1 |

## 解释口径

- 质量检查是本地结构检查：文件存在、一级标题、关键章节/情景/来源/表格/占位符，以及评估报告是否避免目标价/评级类市场定价结论。
- 与旧版对比是与 runner 启动前搬入 `备份/` 的旧文件做大小、行数、二级标题、URL、表格行数对比；不是逐句事实复核。
- 会议 file-run 是新增专题文件，runner 没有旧版 from/to，因此没有备份项可比。
