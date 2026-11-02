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
        one = re.fullmatch(r'topic="([^"]+)"', arguments.strip())
        several = re.fullmatch(r'topics=\[([^\]]*)\]', " ".join(arguments.split()))
        if one:
            topics.add(one.group(1))
        elif several:
            topics.update(re.findall(r'"([^"]+)"', several.group(1)))
        else:
            raise AssertionError('get_guide must be written as get_guide(topic="...") or get_guide(topics=[...]): '
                                 + arguments)
    return topics


def first_call_naming(text, topic):
    """Where the skill first reads that topic, alone or among several."""
    for match in CALL.finditer(text):
        if topic in named_topics(match.group(0)):
            return match.start()
    raise AssertionError("no get_guide call names " + topic)


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
                self.assertLess(text.index("`whoami`"), first_call_naming(text, topic))
                self.assertIn("guideVersion", text)


if __name__ == "__main__":
    unittest.main()
