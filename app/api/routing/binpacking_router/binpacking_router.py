from fastapi import APIRouter
from schema.model import LoadingData
from api.routing.binpacking_router.utils import is_volume_correct, create_dataframe
from src.load_combinations_generator import LoadCombinationMaker
from src.items_packing import ItemsPacking

binpacking_router = APIRouter(prefix="/v1")

@binpacking_router.post("/binpacking")
async def create_binpacking(input_data: LoadingData):
    vehicle, dispatch = create_dataframe(input_data)
    is_correct = is_volume_correct(vehicle=vehicle, dispatch=dispatch)
    if not is_correct:
        return {"success": False,
               "message": "Selected Trucks volume is smaller than dispatch volume"}

    packers = []
    combinations = LoadCombinationMaker(vehicle, dispatch).get_sorted_combinations()
    packer = ItemsPacking(combinations, vehicle, dispatch).pack_items_to_bin()
    packers.append(packer)
    while True:
        if len(packers[-1].bins[0].unfitted_items ) > 0:
            packer = ItemsPacking(combinations, vehicle, dispatch).pack_items_to_bin(packer.bins[0], unfit=True)
            packers.append(packer)
            continue
        break

    data = {}
    for idx, packer in enumerate(packers):
        packer_data = []
        for box in packer.bins:
            box_data = {}
            volume = box.width * box.height * box.depth
            box_data['box_name'] = box.partno
            box_data['volume'] = volume
            box_data['items'] = []  # <- initialize list here
            for item in box.items:
                item_data = {
                    "name": item.partno,
                    "type": item.name,
                    "color": item.color,
                    "position": item.position,
                    "rotation_type": item.rotation_type,
                    "item_length": item.width,
                    "item_width": item.height,
                    "item_height": item.depth,
                    "item_volume": float(item.width) * float(item.height) * float(item.depth),
                    "item_weight": float(item.weight),
                }
                box_data['items'].append(item_data)  # <- append each item
            packer_data.append(box_data)
        data[idx] = packer_data

    return data