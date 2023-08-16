import os.path


from pentest_helper.init_functions import init_mission, init_host


def test_init_mission_with_path_only(tmp_path):
    mission_path = os.path.join(tmp_path, "box1")
    init_mission(mission_path)

    assert os.path.exists(mission_path)

    assert os.path.isfile(os.path.join(mission_path, "notes.md"))
    assert os.path.isfile(os.path.join(mission_path, "passwords.txt"))
    assert os.path.isfile(os.path.join(mission_path, "users.txt"))
    assert os.path.isfile(os.path.join(mission_path, "wordlist.txt"))

    assert os.path.isdir(os.path.join(mission_path, "hosts"))
    assert os.path.isdir(os.path.join(mission_path, "scans"))


def test_init_mission_with_path_and_hosts(tmp_path):
    mission_path = os.path.join(tmp_path, "box1")
    init_mission(mission_path, hosts=["1.1.1.1", "2.2.2.2"])

    assert os.path.exists(mission_path)

    assert os.path.isfile(os.path.join(mission_path, "notes.md"))
    assert os.path.isfile(os.path.join(mission_path, "passwords.txt"))
    assert os.path.isfile(os.path.join(mission_path, "users.txt"))
    assert os.path.isfile(os.path.join(mission_path, "wordlist.txt"))

    assert os.path.isdir(os.path.join(mission_path, "hosts"))
    assert os.path.isdir(os.path.join(mission_path, "scans"))

    # Test for host 1.1.1.1
    assert os.path.isfile(os.path.join(mission_path, "hosts", "1.1.1.1", "passwords.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "1.1.1.1", "users.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "1.1.1.1", "wordlist.txt"))

    assert os.path.isdir(os.path.join(mission_path, "hosts", "1.1.1.1", "scans"))

    # Test for host 2.2.2.2
    assert os.path.isfile(os.path.join(mission_path, "hosts", "2.2.2.2", "passwords.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "2.2.2.2", "users.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "2.2.2.2", "wordlist.txt"))

    assert os.path.isdir(os.path.join(mission_path, "hosts", "2.2.2.2", "scans"))


def test_init_mission_then_init_host(tmp_path):
    mission_path = os.path.join(tmp_path, "box1")
    init_mission(mission_path)
    init_host(mission_path, "1.1.1.1")
    init_host(mission_path, "2.2.2.2")
    assert os.path.exists(mission_path)

    assert os.path.isfile(os.path.join(mission_path, "notes.md"))
    assert os.path.isfile(os.path.join(mission_path, "passwords.txt"))
    assert os.path.isfile(os.path.join(mission_path, "users.txt"))
    assert os.path.isfile(os.path.join(mission_path, "wordlist.txt"))

    assert os.path.isdir(os.path.join(mission_path, "hosts"))
    assert os.path.isdir(os.path.join(mission_path, "scans"))

    # Test for host 1.1.1.1
    assert os.path.isfile(os.path.join(mission_path, "hosts", "1.1.1.1", "passwords.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "1.1.1.1", "users.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "1.1.1.1", "wordlist.txt"))

    assert os.path.isdir(os.path.join(mission_path, "hosts", "1.1.1.1", "scans"))

    # Test for host 2.2.2.2
    assert os.path.isfile(os.path.join(mission_path, "hosts", "2.2.2.2", "passwords.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "2.2.2.2", "users.txt"))
    assert os.path.isfile(os.path.join(mission_path, "hosts", "2.2.2.2", "wordlist.txt"))

    assert os.path.isdir(os.path.join(mission_path, "hosts", "2.2.2.2", "scans"))
