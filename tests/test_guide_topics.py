from pathlib import Path
import re
import unittest


PLUGIN = Path(__file__).resolve().parents[1] / "plugins/agentdeck"
SERVED_TOPICS = {"overview", "create", "prompt-design", "industry-patterns", "test", "evaluation",
                 "update", "go-live", "server-rules"}
OWN_TOPIC = {"create-agent": "create", "test-agent": "test", "update-agent": "update", "go-live": "go-live"}
CALL = re.compile(r"get_guide\(([^)]*)\)")


def named_topics(text):
    topics = set()
    for arguments in CALL.findall(text):
        match = re.fullmatch(r'topic="([^"]+)"', arguments.strip())
        if not match:
            raise AssertionError("get_guide must be written as get_guide(topic=\"...\"): " + arguments)
        topics.add(match.group(1))
    return topics


class GuideTopicsTest(unittest.TestCase):
    def test_every_named_topic_is_one_the_server_serves(self):
        for path in PLUGIN.rglob("*.md"):
            with self.subTest(path=path.relative_to(PLUGIN)):
                self.assertLessEqual(named_topics(path.read_text()), SERVED_TOPICS)

    def test_each_skill_reads_whoami_and_then_its_own_topic(self):
        for skill, topic in OWN_TOPIC.items():
            with self.subTest(skill=skill):
                text = (PLUGIN / "skills" / skill / "SKILL.md").read_text()
                self.assertIn(topic, named_topics(text))
                self.assertLess(text.index("`whoami`"), text.index('get_guide(topic="' + topic + '")'))
                self.assertIn("guideVersion", text)


if __name__ == "__main__":
    unittest.main()
