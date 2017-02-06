from spade.core.project import Project

class TestProjectWorkflow():
    def test_project_creation(self):
        project = Project("tests/testdb1.sdb")
        assert project is not None

