在获得预测的碳谱数据集后，可使用 tiqu.py 脚本对预测的原始碳谱数据进行提取。该脚本同样支持对实测数据进行初步提取分析，但由于实测谱图容易受到仪器性能及化合物纯度的显著影响，建议对其实测结果进行人工判断和筛选。提取得到的结果将保存为名为 chunchemical_shifts.csv 的文件，用户可据此按需构建或比对自定义数据集。

在获得 chunchemical_shifts.csv 文件后，可使用 bijiao.py 脚本选择合适的计算模式以生成所需的比较结果。当以单一实测数据与预测数据集进行比对时，程序会生成 jkytestn.csv 文件，主要用于可能性筛选分析。

文件说明如下：

idnames.tab：记录数据集中化合物的 ID、化学名称及对应分子量。

mols.rar：包含用于预测的分子 .mol 文件集合。

jkytestn.xlsx：在 jkytestn.csv 基础上添加了分子量信息，可根据分子量及化学位移距离排序，用于筛选潜在匹配的化合物。

与此同时，pagechakan 文件夹包含一个基于 Flask 的网页项目，用于查看原始预测的碳谱数据或已转换为 CSV 格式的实测谱图数据。
将该文件夹下载至本地后，请首先根据 requirements.txt 安装所需依赖，并在 config.py 文件中根据实际数据存储路径进行相应修改。
完成配置后，在项目根目录下执行命令：

python app.py


即可在本地浏览器通过端口 5000 访问并使用该网页界面。

############################################################

After obtaining the predicted carbon NMR dataset, the script tiqu.py can be used to extract the raw predicted spectra. This script can also perform preliminary extraction from experimental spectra; however, since experimental data are highly influenced by instrument conditions and compound purity, manual verification and curation are strongly recommended. The extraction results are saved as a file named chunchemical_shifts.csv, which can be customized for dataset comparison as needed.

Once the chunchemical_shifts.csv file is generated, the script bijiao.py can be used to perform the desired comparison by selecting an appropriate calculation mode. When comparing a single experimental spectrum with the predicted dataset, the program produces a file named jkytestn.csv, which serves as the primary output for candidate screening.

The following auxiliary files are included:

idnames.tab – Contains compound IDs, chemical names, and corresponding molecular weights in the dataset.

mols.rar – A collection of .mol files representing the molecular structures used for prediction.

jkytestn.xlsx – An extended version of jkytestn.csv with molecular weight information added, allowing for candidate filtering and ranking based on molecular weight and chemical shift distance.

Meanwhile, the pagechakan directory contains a Flask-based web application designed for visualizing either the raw predicted carbon spectra or the experimental spectra converted into CSV format.
After downloading the folder to your local environment, install the required dependencies specified in requirements.txt, and modify the file paths in config.py according to your actual data storage locations.
Once configured, run the following command in the project’s root directory:

python app.py


The web interface can then be accessed locally through your browser at port 5000.
