import qsea
import logging

logging.basicConfig(level=logging.DEBUG)

prefix = 'pre2'

qsea.test()

print(qsea.__file__)


ws = qsea.OpenConnection(qlik_url, header_user)

qsea.GetAppID(ws, 'Qlik Engine Test')

app = qsea.App(ws, 'Qlik Engine Test')

app.load()

app.measures.add('NewMs' + prefix, definition = 'NewMsDef' + prefix, description = 'desc' + prefix, label = 'lbl' + prefix, labelExpression = 'lblEx' + prefix)