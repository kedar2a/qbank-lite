# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/Users/cjshaw/Documents/Projects/CLIx/qbank-lite'],
             binaries=None,
             datas=None,
             hiddenimports=['dlkit',
                            'dlkit.mongo',
                            'dlkit.mongo.assessment.managers',
                            'dlkit.mongo.assessment.sessions',
                            'dlkit.mongo.assessment.objects',
                            'dlkit.mongo.logging_.managers',
                            'dlkit.mongo.logging_.sessions',
                            'dlkit.mongo.logging_.objects',
                            'dlkit.services',
                            'dlkit.services.assessment',
                            'dlkit.services.logging_',
                            'records'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='main.app',
             icon=None,
             bundle_identifier=None)
