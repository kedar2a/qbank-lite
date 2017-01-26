import os

from bs4 import BeautifulSoup

from dlkit_runtime.configs import FILESYSTEM_ASSET_CONTENT_TYPE
from dlkit_runtime.primordium import DataInputStream, Type, Id

from nose.tools import *

from testing_utilities import BaseTestCase, get_fixture_repository, get_managers
from urllib import unquote, quote

from records.registry import ASSESSMENT_RECORD_TYPES

import utilities

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ABS_PATH = os.path.abspath(os.path.join(PROJECT_PATH, os.pardir))

SIMPLE_SEQUENCE_RECORD = Type(**ASSESSMENT_RECORD_TYPES['simple-child-sequencing'])


class BaseRepositoryTestCase(BaseTestCase):
    def _create_asset(self):
        form = self._repo.get_asset_form_for_create([])
        form.display_name = 'Test asset'
        asset = self._repo.create_asset(form)

        content_form = self._repo.get_asset_content_form_for_create(asset.ident, [FILESYSTEM_ASSET_CONTENT_TYPE])
        content_form.display_name = 'test asset content'
        content_form.set_data(DataInputStream(self.test_file))
        ac = self._repo.create_asset_content(content_form)

        # need to get the IDs to match, so update it like in the system
        self.test_file.seek(0)
        form = self._repo.get_asset_content_form_for_update(ac.ident)
        form.set_data(DataInputStream(self.test_file))
        self._repo.update_asset_content(form)

        return self._repo.get_asset(asset.ident)

    def num_assets(self, val):
        self.assertEqual(
            self._repo.get_assets().available(),
            int(val)
        )

    def setUp(self):
        super(BaseRepositoryTestCase, self).setUp()
        self.url = '/api/v1/repository'
        self._repo = get_fixture_repository()
        test_file = '{0}/tests/files/sample_movie.MOV'.format(ABS_PATH)

        self.test_file = open(test_file, 'r')

    def tearDown(self):
        super(BaseRepositoryTestCase, self).tearDown()
        self.test_file.close()


class AssetContentTests(BaseRepositoryTestCase):
    def create_assessment_offered_for_item(self, bank_id, item_id):
        if isinstance(bank_id, basestring):
            bank_id = utilities.clean_id(bank_id)
        if isinstance(item_id, basestring):
            item_id = utilities.clean_id(item_id)

        bank = get_managers()['am'].get_bank(bank_id)
        form = bank.get_assessment_form_for_create([SIMPLE_SEQUENCE_RECORD])
        form.display_name = 'a test assessment'
        form.description = 'for testing with'
        new_assessment = bank.create_assessment(form)

        bank.add_item(new_assessment.ident, item_id)

        form = bank.get_assessment_offered_form_for_create(new_assessment.ident, [])
        new_offered = bank.create_assessment_offered(form)

        return new_offered

    def create_item_with_image(self):
        url = '{0}/items'.format(self.assessment_url)
        self._image_in_question.seek(0)
        req = self.app.post(url,
                            upload_files=[('qtiFile',
                                           self._filename(self._image_in_question),
                                           self._image_in_question.read())])
        self.ok(req)
        return self.json(req)

    def create_item_with_image_in_choices(self):
        url = '{0}/items'.format(self.assessment_url)
        self._images_in_choices.seek(0)
        req = self.app.post(url,
                            upload_files=[('qtiFile',
                                           self._filename(self._images_in_choices),
                                           self._images_in_choices.read())])
        self.ok(req)
        return self.json(req)

    def create_upload_item(self):
        url = '{0}/items'.format(self.assessment_url)
        self._generic_upload_test_file.seek(0)
        req = self.app.post(url,
                            upload_files=[('qtiFile', 'testFile', self._generic_upload_test_file.read())])
        self.ok(req)
        return self.json(req)

    def create_taken_for_item(self, bank_id, item_id):
        if isinstance(bank_id, basestring):
            bank_id = utilities.clean_id(bank_id)
        if isinstance(item_id, basestring):
            item_id = utilities.clean_id(item_id)

        bank = get_managers()['am'].get_bank(bank_id)

        new_offered = self.create_assessment_offered_for_item(bank_id, item_id)

        form = bank.get_assessment_taken_form_for_create(new_offered.ident, [])
        taken = bank.create_assessment_taken(form)
        return taken, new_offered

    def setUp(self):
        super(AssetContentTests, self).setUp()
        self.asset = self._create_asset()
        asset_content = self.asset.get_asset_contents().next()
        self.assessment_url = '/api/v1/assessment/banks/{0}'.format(unquote(str(self._repo.ident)))
        self.url = '{0}/repositories/{1}/assets/{2}/contents/{3}'.format(self.url,
                                                                         unquote(str(self._repo.ident)),
                                                                         unquote(str(self.asset.ident)),
                                                                         unquote(str(asset_content.ident)))

        self._generic_upload_test_file = open('{0}/tests/files/generic_upload_test_file.zip'.format(ABS_PATH), 'r')
        self._logo_upload_test_file = open('{0}/tests/files/Epidemic2.sltng'.format(ABS_PATH), 'r')
        self._replacement_image_file = open('{0}/tests/files/replacement_image.png'.format(ABS_PATH), 'r')
        self._images_in_choices = open('{0}/tests/files/qti_file_with_images.zip'.format(ABS_PATH), 'r')
        self._image_in_question = open('{0}/tests/files/mw_sentence_with_audio_file.zip'.format(ABS_PATH), 'r')

    def tearDown(self):
        """
        Remove the test user from all groups in Membership
        Start from the smallest groupId because need to
        remove "parental" roles like for DepartmentAdmin / DepartmentOfficer
        """
        super(AssetContentTests, self).tearDown()

        self._generic_upload_test_file.close()
        self._logo_upload_test_file.close()
        self._replacement_image_file.close()
        self._images_in_choices.close()
        self._image_in_question.close()

    def test_can_get_asset_content_file(self):
        req = self.app.get(self.url)
        self.ok(req)
        self.test_file.seek(0)
        self.assertEqual(
            req.body,
            self.test_file.read()
        )

    def test_unknown_asset_content_extensions_preserved(self):
        upload_item = self.create_upload_item()
        taken, offered = self.create_taken_for_item(self._repo.ident, Id(upload_item['id']))
        url = '{0}/assessmentstaken/{1}/questions/{2}/submit'.format(self.assessment_url,
                                                                     unquote(str(taken.ident)),
                                                                     unquote(upload_item['id']))

        self._logo_upload_test_file.seek(0)
        req = self.app.post(url,
                            upload_files=[('submission', 'Epidemic2.sltng', self._logo_upload_test_file.read())])
        self.ok(req)

        url = '/api/v1/repository/repositories/{0}/assets'.format(unquote(str(self._repo.ident)))
        req = self.app.get(url)
        self.ok(req)
        data = self.json(req)
        self.assertEqual(len(data), 2)
        for asset in data:
            if asset['id'] != str(self.asset.ident):
                self.assertTrue('.sltng' in asset['assetContents'][0]['url'])
                self.assertEqual('asset-content-genus-type%3Asltng%40ODL.MIT.EDU',
                                 asset['assetContents'][0]['genusTypeId'])

    def test_can_update_asset_content_with_new_file(self):
        req = self.app.get(self.url)
        self.ok(req)
        asset_content = self.asset.get_asset_contents().next()
        original_genus_type = str(asset_content.genus_type)
        original_file_name = asset_content.display_name.text
        original_on_disk_name = asset_content.get_url()
        original_id = str(asset_content.ident)

        self._replacement_image_file.seek(0)
        req = self.app.put(self.url,
                           upload_files=[('inputFile',
                                          self._filename(self._replacement_image_file),
                                          self._replacement_image_file.read())])
        self.ok(req)
        data = self.json(req)
        asset_content = data['assetContents'][0]
        self.assertNotEqual(
            original_genus_type,
            asset_content['genusTypeId']
        )
        self.assertIn('png', asset_content['genusTypeId'])
        self.assertNotEqual(
            original_file_name,
            asset_content['displayName']['text']
        )
        self.assertEqual(
            original_on_disk_name.split('.')[0],
            asset_content['url'].split('.')[0]
        )
        self.assertEqual(
            original_id,
            asset_content['id']
        )
        self.assertIn(
            self._replacement_image_file.name.split('/')[-1],
            asset_content['displayName']['text']
        )

    def test_updated_asset_content_in_question_shows_up_properly_in_item_qti(self):
        item = self.create_item_with_image()
        taken, offered = self.create_taken_for_item(self._repo.ident, Id(item['id']))
        url = '{0}/assessmentstaken/{1}/questions?qti'.format(self.assessment_url,
                                                              unquote(str(taken.ident)))

        req = self.app.get(url)
        self.ok(req)
        data = self.json(req)['data']
        soup = BeautifulSoup(data[0]['qti'], 'xml')
        image = soup.find('img')

        req = self.app.get(image['src'])
        self.ok(req)
        headers = req.header_dict
        self.assertIn('image/png', headers['content-type'])
        self.assertIn('.png', headers['content-disposition'])
        original_content_length = headers['content-length']

        content_url = image['src']
        self._logo_upload_test_file.seek(0)
        req = self.app.put(content_url,
                           upload_files=[('inputFile',
                                          self._filename(self._logo_upload_test_file),
                                          self._logo_upload_test_file.read())])
        self.ok(req)

        req = self.app.get(url)
        self.ok(req)
        data = self.json(req)['data']
        soup = BeautifulSoup(data[0]['qti'], 'xml')
        image = soup.find('img')

        req = self.app.get(image['src'])
        self.ok(req)
        headers = req.header_dict
        self.assertNotIn('image/png', headers['content-type'])
        self.assertIn('.sltng', headers['content-disposition'])
        self.assertNotEqual(original_content_length, headers['content-length'])

    def test_updated_asset_content_in_choices_shows_up_properly_in_item_qti(self):
        item = self.create_item_with_image_in_choices()
        taken, offered = self.create_taken_for_item(self._repo.ident, Id(item['id']))
        url = '{0}/assessmentstaken/{1}/questions?qti'.format(self.assessment_url,
                                                              unquote(str(taken.ident)))

        req = self.app.get(url)
        self.ok(req)
        data = self.json(req)['data']
        soup = BeautifulSoup(data[0]['qti'], 'xml')
        image = soup.find('img')

        req = self.app.get(image['src'])
        self.ok(req)
        headers = req.header_dict
        self.assertIn('image/png', headers['content-type'])
        self.assertIn('.png', headers['content-disposition'].lower())
        original_content_length = headers['content-length']

        content_url = image['src']
        self._logo_upload_test_file.seek(0)
        req = self.app.put(content_url,
                           upload_files=[('inputFile',
                                          self._filename(self._logo_upload_test_file),
                                          self._logo_upload_test_file.read())])
        self.ok(req)

        req = self.app.get(url)
        self.ok(req)
        data = self.json(req)['data']
        soup = BeautifulSoup(data[0]['qti'], 'xml')
        image = soup.find('img')

        req = self.app.get(image['src'])
        self.ok(req)
        headers = req.header_dict
        self.assertNotIn('image/png', headers['content-type'])
        self.assertIn('.sltng', headers['content-disposition'])
        self.assertNotEqual(original_content_length, headers['content-length'])


class AssetQueryTests(BaseRepositoryTestCase):
    def setUp(self):
        super(AssetQueryTests, self).setUp()
        self.url = '{0}/repositories/{1}/assets'.format(self.url,
                                                        unquote(str(self._repo.ident)))

        self._video_upload_test_file = open('{0}/tests/files/video-js-test.mp4'.format(ABS_PATH), 'r')
        self._caption_upload_test_file = open('{0}/tests/files/video-js-test-en.vtt'.format(ABS_PATH), 'r')

    def tearDown(self):
        """
        Remove the test user from all groups in Membership
        Start from the smallest groupId because need to
        remove "parental" roles like for DepartmentAdmin / DepartmentOfficer
        """
        super(AssetQueryTests, self).tearDown()

        self._video_upload_test_file.close()
        self._caption_upload_test_file.close()

    def test_can_get_assets_with_valid_content_urls(self):
        self._video_upload_test_file.seek(0)
        req = self.app.post(self.url,
                            upload_files=[('inputFile', 'video-js-test.mp4', self._video_upload_test_file.read())])
        self.ok(req)
        data = self.json(req)

        self._caption_upload_test_file.seek(0)
        req = self.app.post(self.url,
                            upload_files=[('inputFile', 'video-js-test-en.vtt', self._caption_upload_test_file.read())])
        self.ok(req)

        url = '{0}?fullUrls'.format(self.url)
        req = self.app.get(url)
        self.ok(req)
        data = self.json(req)

        self.assertEqual(len(data), 1)
        asset = data[0]
        self.assertEqual(
            len(asset['assetContents']),
            2
        )

        for index, asset_content in enumerate(asset['assetContents']):
            if index == 0:
                self.assertEqual(
                    asset_content['genusTypeId'],
                    'asset-content-genus-type%3Amp4%40ODL.MIT.EDU'
                )
            else:
                self.assertEqual(
                    asset_content['genusTypeId'],
                    'asset-content-genus-type%3Avtt%40ODL.MIT.EDU'
                )
            self.assertNotIn(
                'datastore/repository/AssetContent/',
                asset_content['url']
            )
            self.assertEqual(
                '/api/v1/repository/repositories/{0}/assets/{1}/contents/{2}'.format(asset['assignedRepositoryIds'][0],
                                                                                     asset['id'],
                                                                                     asset_content['id']),
                asset_content['url']
            )


class AssetUploadTests(BaseRepositoryTestCase):
    def setUp(self):
        super(AssetUploadTests, self).setUp()
        self.url = '{0}/repositories/{1}/assets'.format(self.url,
                                                        unquote(str(self._repo.ident)))

        self._video_upload_test_file = open('{0}/tests/files/video-js-test.mp4'.format(ABS_PATH), 'r')
        self._caption_upload_test_file = open('{0}/tests/files/video-js-test-en.vtt'.format(ABS_PATH), 'r')

    def tearDown(self):
        """
        Remove the test user from all groups in Membership
        Start from the smallest groupId because need to
        remove "parental" roles like for DepartmentAdmin / DepartmentOfficer
        """
        super(AssetUploadTests, self).tearDown()

        self._video_upload_test_file.close()
        self._caption_upload_test_file.close()

    def test_can_upload_video_files_to_repository(self):
        self._video_upload_test_file.seek(0)
        req = self.app.post(self.url,
                            upload_files=[('inputFile', 'video-js-test.mp4', self._video_upload_test_file.read())])
        self.ok(req)
        data = self.json(req)
        self.assertEqual(
            len(data['assetContents']),
            1
        )
        self.assertEqual(
            data['assetContents'][0]['genusTypeId'],
            'asset-content-genus-type%3Amp4%40ODL.MIT.EDU'
        )

        # because this is hidden / stripped out
        self.assertNotIn(
            'asset_content_record_type%3Afilesystem%40odl.mit.edu',
            data['recordTypeIds']
        )
        self.assertIn(
            'datastore/repository/AssetContent/',
            data['assetContents'][0]['url']
        )
        self.assertEqual(
            'video-js-test.mp4',
            data['assetContents'][0]['displayName']['text']
        )

    def test_can_create_asset_with_flag_to_return_valid_url(self):
        self._video_upload_test_file.seek(0)
        req = self.app.post(self.url,
                            params={'returnUrl': True},
                            upload_files=[('inputFile', 'video-js-test.mp4', self._video_upload_test_file.read())])
        self.ok(req)
        data = self.json(req)
        self.assertEqual(
            len(data['assetContents']),
            1
        )
        self.assertEqual(
            data['assetContents'][0]['genusTypeId'],
            'asset-content-genus-type%3Amp4%40ODL.MIT.EDU'
        )

        # because this is hidden / stripped out
        self.assertNotIn(
            'asset_content_record_type%3Afilesystem%40odl.mit.edu',
            data['recordTypeIds']
        )
        self.assertNotIn(
            'datastore/repository/AssetContent/',
            data['assetContents'][0]['url']
        )
        self.assertEqual(
            '/api/v1/repository/repositories/{0}/assets/{1}/contents/{2}'.format(data['assignedRepositoryIds'][0],
                                                                                 data['id'],
                                                                                 data['assetContents'][0]['id']),
            data['assetContents'][0]['url']
        )
        self.assertEqual(
            'video-js-test.mp4',
            data['assetContents'][0]['displayName']['text']
        )

    def test_can_upload_caption_vtt_files_to_repository(self):
        self._caption_upload_test_file.seek(0)
        req = self.app.post(self.url,
                            upload_files=[('inputFile', 'video-js-test-en.vtt', self._caption_upload_test_file.read())])
        self.ok(req)
        data = self.json(req)
        self.assertEqual(
            len(data['assetContents']),
            1
        )
        self.assertEqual(
            data['assetContents'][0]['genusTypeId'],
            'asset-content-genus-type%3Avtt%40ODL.MIT.EDU'
        )

        # because this is hidden / stripped out
        self.assertNotIn(
            'asset_content_record_type%3Afilesystem%40odl.mit.edu',
            data['recordTypeIds']
        )
        self.assertIn(
            'datastore/repository/AssetContent/',
            data['assetContents'][0]['url']
        )
        self.assertEqual(
            'video-js-test-en.vtt',
            data['assetContents'][0]['displayName']['text']
        )

    def test_caption_and_video_files_uploaded_as_asset_contents_on_same_asset(self):
        self._video_upload_test_file.seek(0)
        req = self.app.post(self.url,
                            upload_files=[('inputFile', 'video-js-test.mp4', self._video_upload_test_file.read())])
        self.ok(req)
        data = self.json(req)
        self.assertEqual(
            len(data['assetContents']),
            1
        )
        asset_id = data['id']
        self.assertEqual(
            data['displayName']['text'],
            'video_js_test'
        )

        self._caption_upload_test_file.seek(0)
        req = self.app.post(self.url,
                            upload_files=[('inputFile', 'video-js-test-en.vtt', self._caption_upload_test_file.read())])
        self.ok(req)
        data = self.json(req)
        self.assertEqual(
            len(data['assetContents']),
            2
        )
        self.assertEqual(
            asset_id,
            data['id']
        )
        self.assertEqual(
            data['displayName']['text'],
            'video_js_test'
        )

        self.assertEqual(
            data['assetContents'][0]['genusTypeId'],
            'asset-content-genus-type%3Amp4%40ODL.MIT.EDU'
        )
        self.assertIn(
            'datastore/repository/AssetContent/',
            data['assetContents'][0]['url']
        )
        self.assertEqual(
            'video-js-test.mp4',
            data['assetContents'][0]['displayName']['text']
        )

        self.assertEqual(
            data['assetContents'][1]['genusTypeId'],
            'asset-content-genus-type%3Avtt%40ODL.MIT.EDU'
        )
        self.assertIn(
            'datastore/repository/AssetContent/',
            data['assetContents'][1]['url']
        )
        self.assertEqual(
            'video-js-test-en.vtt',
            data['assetContents'][1]['displayName']['text']
        )