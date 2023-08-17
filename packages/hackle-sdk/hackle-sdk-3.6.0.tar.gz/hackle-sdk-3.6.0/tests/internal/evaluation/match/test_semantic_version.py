from hackle.internal.evaluation.match.semantic_version import SemanticVersion
from tests import base


class SemanticVersionTest(base.BaseTest):

    def test_parse_string_타입이_아니면_None_리턴(self):
        self.assertIsNone(self.v(42))

    def test_parse_invalid_format(self):
        self.assertIsNone(self.v('01.0.0'))
        self.assertIsNone(self.v('1.01.0'))
        self.assertIsNone(self.v('1.1.01'))
        self.assertIsNone(self.v('2.x'))
        self.assertIsNone(self.v('2.3.x'))
        self.assertIsNone(self.v('2.3.1.4'))
        self.assertIsNone(self.v('2.3.1*beta'))
        self.assertIsNone(self.v('2.3.1-beta*'))
        self.assertIsNone(self.v('2.4.1-beta_4'))

    def test_parse_semantic_core_version(self):
        self.verify('1.0.0', 1, 0, 0, [], [])
        self.verify('14.165.14', 14, 165, 14, [], [])

    def test_parse_semantic_version_with_prerelease(self):
        self.verify('1.0.0-beta1', 1, 0, 0, ['beta1'], [])
        self.verify('1.0.0-beta.1', 1, 0, 0, ['beta', '1'], [])
        self.verify('1.0.0-x.y.z', 1, 0, 0, ['x', 'y', 'z'], [])

    def test_parse_semantic_version_with_build(self):
        self.verify('1.0.0+build1', 1, 0, 0, [], ['build1'])
        self.verify('1.0.0+build.1', 1, 0, 0, [], ['build', '1'])
        self.verify('1.0.0+1.2.3', 1, 0, 0, [], ['1', '2', '3'])

    def test_parse_semantic_version_with_prerelease_and_build(self):
        self.verify('1.0.0-alpha.3.rc.5+build.53', 1, 0, 0, ['alpha', '3', 'rc', '5'], ['build', '53'])

    def test_minor_patch가_없는경우_0으로_채워준다(self):
        self.verify('15', 15, 0, 0, [], [])
        self.verify('15.143', 15, 143, 0, [], [])
        self.verify('15-x.y.z', 15, 0, 0, ['x', 'y', 'z'], [])
        self.verify('15-x.y.z+a.b.c', 15, 0, 0, ['x', 'y', 'z'], ['a', 'b', 'c'])

    def test_core_버전만_있는경우_core_버전이_같으면_같은_버전이다(self):
        v1 = self.v('2.3.4')
        v2 = self.v('2.3.4')
        self.assertTrue(v1 == v2)

    def test_core_prerelease_버전이_모두_같아야_같은_버전이다(self):
        self.assertTrue(self.v('2.3.4-beta.1') == self.v('2.3.4-beta.1'))

    def test_prerelease_버전이_다르면_다른_버전이다(self):
        self.assertTrue(self.v('2.3.4-beta.1') != self.v('2.3.4-beta.2'))

    def test_build가_달라도_나머지가_같으면_같은버전이다(self):
        self.assertTrue(self.v('2.3.4+build.111') == self.v('2.3.4+build.222'))
        self.assertTrue(self.v('2.3.4-beta.1+build.111') == self.v('2.3.4-beta.1+build.222'))

    def test_major를_가장_먼저_비교한다(self):
        self.assertTrue(self.v('4.5.7') > self.v('3.5.7'))
        self.assertTrue(self.v('2.5.7') < self.v('3.5.7'))

    def test_major가_같으면_minor를_비교한다(self):
        self.assertTrue(self.v('3.6.7') > self.v('3.5.7'))
        self.assertTrue(self.v('3.4.7') < self.v('3.5.7'))

    def test_minor까지_같으면_patch를_비교한다(self):
        self.assertTrue(self.v('3.5.8') > self.v('3.5.7'))
        self.assertTrue(self.v('3.5.6') < self.v('3.5.7'))

    def test_정식_배포_버전이_더_높은_버전이다(self):
        self.assertTrue(self.v('3.5.7') > self.v('3.5.7-beta'))
        self.assertTrue(self.v('3.5.7-alpha') < self.v('3.5.7'))

    def test_prerelease_숫자로만_구성된_식별자는_수의_크기로_비교한다(self):
        self.assertTrue(self.v('3.5.7-1') < self.v('3.5.7-2'))
        self.assertTrue(self.v('3.5.7-1.1') < self.v('3.5.7-1.2'))
        self.assertTrue(self.v('3.5.7-11') > self.v('3.5.7-2'))

    def test_prerelease_알파벳이_포함된_경우에는_아스키_문자열_정렬을_한다(self):
        self.assertTrue(self.v('3.5.7-a') == self.v('3.5.7-a'))
        self.assertTrue(self.v('3.5.7-a') < self.v('3.5.7-b'))
        self.assertTrue(self.v('3.5.7-az') > self.v('3.5.7-ab'))
        self.assertTrue(self.v('3.5.7-alpha') < self.v('3.5.7-beta'))

    def test_prerelease_숫자로만_구성된_식별자는_어떤_경우에도_문자와_붙임표가_있는_식별자보다_낮은_우선순위로_여긴다(self):
        self.assertTrue(self.v('3.5.7-9') < self.v('3.5.7-a'))
        self.assertTrue(self.v('3.5.7-9') < self.v('3.5.7-a-9'))
        self.assertTrue(self.v('3.5.7-beta') > self.v('3.5.7-1'))

    def test_prerelease_앞선_식별자가_모두_같은_배포_전_버전의_경우에는_필드_수가_많은_쪽이_더_높은_우선순위를_가진다(self):
        self.assertTrue(self.v('3.5.7-alpha') < self.v('3.5.7-alpha.1'))
        self.assertTrue(self.v('3.5.7-1.2.3') < self.v('3.5.7-1.2.3.4'))

    def verify(self, version, major, minor, patch, prerelease, build):
        parsed_version = self.v(version)
        self.assertIsNotNone(parsed_version)
        self.assertEqual(major, parsed_version.core_version.major)
        self.assertEqual(minor, parsed_version.core_version.minor)
        self.assertEqual(patch, parsed_version.core_version.patch)
        self.assertEqual(prerelease, parsed_version.prerelease.identifiers)
        self.assertEqual(build, parsed_version.build.identifiers)

    @staticmethod
    def v(version):
        return SemanticVersion.parse_or_none(version)
