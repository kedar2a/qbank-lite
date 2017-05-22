# -*- mode: python -*-

import os

block_cipher = None

a = Analysis(['main.py'],
             pathex=[os.getcwd()],
             binaries=None,
             datas=[('unplatform/*', 'unplatform')],
             hiddenimports=['_cffi_backend',
                            'six',
                            'sympy',
                            'bs4',
                            'lxml',
                            'dlkit',
                            'dlkit.filesystem_adapter',
                            'dlkit.filesystem_adapter.osid.managers',
                            'dlkit.filesystem_adapter.osid.sessions',
                            'dlkit.filesystem_adapter.osid.objects',
                            'dlkit.filesystem_adapter.repository.managers',
                            'dlkit.filesystem_adapter.repository.sessions',
                            'dlkit.filesystem_adapter.repository.objects',
                            'dlkit.json_',
                            'dlkit.json_.assessment.managers',
                            'dlkit.json_.assessment.sessions',
                            'dlkit.json_.assessment.objects',
                            'dlkit.json_.assessment_authoring.managers',
                            'dlkit.json_.assessment_authoring.sessions',
                            'dlkit.json_.assessment_authoring.objects',
                            'dlkit.json_.hierarchy.managers',
                            'dlkit.json_.hierarchy.sessions',
                            'dlkit.json_.hierarchy.objects',
                            'dlkit.json_.logging_.managers',
                            'dlkit.json_.logging_.sessions',
                            'dlkit.json_.logging_.objects',
                            'dlkit.json_.relationship.managers',
                            'dlkit.json_.relationship.sessions',
                            'dlkit.json_.relationship.objects',
                            'dlkit.json_.repository.managers',
                            'dlkit.json_.repository.sessions',
                            'dlkit.json_.repository.objects',
                            'dlkit.json_.resource.managers',
                            'dlkit.json_.resource.sessions',
                            'dlkit.json_.resource.objects',
                            'dlkit.primordium.locale.objects',
                            'dlkit.services',
                            'dlkit.services.assessment',
                            'dlkit.services.hierarchy',
                            'dlkit.services.logging_',
                            'dlkit.services.relationship',
                            'dlkit.services.repository',
                            'dlkit.services.resource',
                            'dlkit.records',
                            'dlkit.records.assessment',
                            'dlkit.records.assessment.basic',
                            'dlkit.records.assessment.basic.assessment_records',
                            'dlkit.records.assessment.basic.base_records',
                            'dlkit.records.assessment.basic.feedback_answer_records',
                            'dlkit.records.assessment.basic.feedback_item_records',
                            'dlkit.records.assessment.basic.file_answer_records',
                            'dlkit.records.assessment.basic.multi_choice_records',
                            'dlkit.records.assessment.basic.simple_records',
                            'dlkit.records.assessment.basic.wrong_answers',
                            'dlkit.records.assessment.clix.assessment_offered_records',
                            'dlkit.records.assessment.clix.magic_item_lookup_sessions',
                            'dlkit.records.assessment.qti',
                            'dlkit.records.assessment.qti.basic',
                            'dlkit.records.assessment.qti.extended_text_interaction',
                            'dlkit.records.assessment.qti.inline_choice_records',
                            'dlkit.records.assessment.qti.numeric_response_records',
                            'dlkit.records.assessment.qti.ordered_choice_records',
                            'dlkit.records.logging.clix.text_blob',
                            'dlkit.records.osid',
                            'dlkit.records.osid.base_records',
                            'dlkit.records.osid.object_records',
                            'dlkit.records.adaptive.multi_choice_questions.randomized_questions'],
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
          console=True )
app = BUNDLE(exe,
             name='main.app',
             icon=None,
             bundle_identifier=None)
