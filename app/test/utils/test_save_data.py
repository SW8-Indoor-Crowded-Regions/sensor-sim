import pytest
from app.utils.save_data import save_data
from app.classes.room import Room

@pytest.fixture
def mock_db(mocker):
    mock_collection = mocker.Mock()
    mock_collection.bulk_write.return_value.modified_count = 2
    db = {"room": mock_collection}
    mocker.patch("app.utils.save_data.get_db", return_value=db)
    return mock_collection

def test_save_data_single_room(mock_db, capsys):
    test_room = Room({"id": "room1", "name": "Single", "type": "Lab"}, 0, 1.0, 1.2, 50.0, [])
    test_room.occupancy = 5
    save_data([test_room])
    mock_db.bulk_write.assert_called_once()
    captured = capsys.readouterr()
    assert "Updated 2 rooms." in captured.out

def test_save_data_no_rooms(mock_db, capsys):
    save_data([])
    mock_db.bulk_write.assert_not_called()
    captured = capsys.readouterr()
    assert "No data to save." in captured.out

def test_save_data_multiple_rooms(mock_db, capsys):
    rooms = []
    for i in range(3):
        room_info = {"id": f"room{i}", "name": "Multi", "type": "Lab"}
        r = Room(room_info, 0, 1.0 + i, 1.2, 100.0, [])
        r.occupancy = i
        rooms.append(r)
    save_data(rooms)
    assert mock_db.bulk_write.call_count == 1
    captured = capsys.readouterr()
    assert "Updated 2 rooms." in captured.out
