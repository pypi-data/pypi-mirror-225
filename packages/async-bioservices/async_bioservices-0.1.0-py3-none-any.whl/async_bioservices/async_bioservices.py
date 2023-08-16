import asyncio
import pandas as pd
from enum import Enum
from bioservices import BioDBNet

import requests

# Import InsecureRequestWarning


# requests.packages.urllib3.disable_warnings()

try:
    from input_database import InputDatabase
    from output_database import OutputDatabase
    from taxon_ids import TaxonIDs
except ImportError:
    from .input_database import InputDatabase
    from .output_database import OutputDatabase
    from .taxon_ids import TaxonIDs


class _AsyncBioservices:
    biodbnet: BioDBNet = None
    
    def __init__(self, quiet: bool):
        if _AsyncBioservices.biodbnet is None:
            biodbnet = BioDBNet(verbose=not quiet)  # Invert quiet to verbose
            biodbnet.services.settings.TIMEOUT = 60
            _AsyncBioservices.biodbnet = biodbnet
            self.biodbnet = _AsyncBioservices.biodbnet
        else:
            self.biodbnet = _AsyncBioservices.biodbnet


async def _async_fetch_info(
    biodbnet: BioDBNet,
    event_loop: asyncio.AbstractEventLoop,
    semaphore: asyncio.Semaphore,
    input_values: list[str],
    input_db: str,
    output_db: list[str],
    taxon_id: int,
    delay: int = 10
) -> pd.DataFrame:
    await semaphore.acquire()
    conversion = await asyncio.to_thread(
        biodbnet.db2db,
        input_db=input_db,
        output_db=output_db,
        input_values=input_values,
        taxon=taxon_id
    )
    semaphore.release()
    
    # If the above db2db conversion didn't work, try again until it does
    if not isinstance(conversion, pd.DataFrame):
        # Errors will occur on a timeouut. If this happens, split our working dataset in two and try again
        first_set: list[str] = input_values[:len(input_values) // 2]
        second_set: list[str] = input_values[len(input_values) // 2:]
        
        await asyncio.sleep(delay)
        first_conversion: pd.DataFrame = await _async_fetch_info(
            biodbnet=biodbnet, event_loop=event_loop, semaphore=semaphore,
            input_values=first_set, input_db=input_db, output_db=output_db,
            taxon_id=taxon_id, delay=delay
        )
        second_conversion: pd.DataFrame = await _async_fetch_info(
            biodbnet=biodbnet, event_loop=event_loop, semaphore=semaphore,
            input_values=second_set, input_db=input_db, output_db=output_db,
            taxon_id=taxon_id, delay=delay
        )
        
        return pd.concat([first_conversion, second_conversion])
    
    return conversion


async def _fetch_gene_info_manager(
    tasks: list[asyncio.Task[pd.DataFrame]],
    batch_length: int,
    quiet: bool
) -> list[pd.DataFrame]:
    results: list[pd.DataFrame] = []
    
    if not quiet:
        print("Collecting genes... ", end="")
    
    task: asyncio.Future[pd.DataFrame]
    for i, task in enumerate(asyncio.as_completed(tasks)):
        results.append(await task)
        if not quiet:
            print(f"\rCollecting genes... {(i + 1) * batch_length} of ~{len(tasks) * batch_length} finished", end="")
    
    return results


def fetch_gene_info(
    input_values: list[str],
    input_db: InputDatabase,
    output_db: OutputDatabase | list[OutputDatabase] = None,
    taxon_id: TaxonIDs | int = TaxonIDs.HOMO_SAPIENS.value,
    delay: int = 5,
    quiet: bool = False,
    remove_duplicates: bool = False,
    concurrency: int = 15
) -> pd.DataFrame:
    """
    This function returns a dataframe with important gene information for future operations in MADRID.
    Fetch gene information from BioDBNet
    :param input_values: A list of genes in "input_db" format
    :param input_db: The input database to use (default: "Ensembl Gene ID")
    :param output_db: The output format to use (default: ["Gene Symbol", "Gene ID", "Chromosomal Location"])
    :param delay: The delay in seconds to wait before trying again if bioDBnet is busy (default: 15)
    :param taxon_id: The taxon ID to use (default: 9606)
    :param quiet: Should the conversions show output or not?
    :param concurrency: The number of concurrent connections to make to BioDBNet
    :return: A dataframe with specified columns as "output_db" (Default is HUGO symbol, Entrez ID, and chromosome start and end positions)
    """
    
    input_values = [str(i) for i in input_values]
    input_db_value = input_db.value
    batch_length: int = 100
    
    output_db_values: list[str]
    if output_db is None:
        output_db_values = [
            OutputDatabase.GENE_SYMBOL.value,
            OutputDatabase.GENE_ID.value,
            OutputDatabase.CHROMOSOMAL_LOCATION.value
        ]
    elif isinstance(output_db, OutputDatabase) or isinstance(output_db, Enum):
        output_db_values = [output_db.value]
    else:
        output_db_values = [str(i.value) for i in output_db]
    
    # Check if input_db_value is in output_db_values
    if input_db_value in output_db_values:
        raise ValueError("Input database cannot be in output database")
    
    if isinstance(taxon_id, TaxonIDs) or isinstance(taxon_id, Enum):
        taxon_id_value: int = int(taxon_id.value)
    else:
        taxon_id_value: int = int(taxon_id)
    
    # biodbnet = BioDBNet()
    biodbnet = _AsyncBioservices(quiet=quiet)
    biodbnet.biodbnet.services.TIMEOUT = 60
    
    dataframe_maps: pd.DataFrame = pd.DataFrame([], columns=output_db_values)
    dataframe_maps.index.name = input_db.value
    
    # Create a list of tasks to be awaited
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    async_tasks = []
    semaphore: asyncio.Semaphore = asyncio.Semaphore(concurrency)
    for i in range(0, len(input_values), batch_length):
        # Define an upper range of values to take from input_values
        # Subtract 1 from batch_length to account for 0-indexing and prevent `i` from grabbing the same value twice
        upper_range = min(i + batch_length, len(input_values))
        task = event_loop.create_task(
            _async_fetch_info(
                biodbnet=biodbnet.biodbnet,
                semaphore=semaphore,
                input_values=input_values[i:upper_range],
                input_db=input_db_value,
                output_db=output_db_values,
                taxon_id=taxon_id_value,
                delay=delay,
                event_loop=event_loop
            )
        )
        
        async_tasks.append(task)
    
    database_convert = event_loop.run_until_complete(
        _fetch_gene_info_manager(tasks=async_tasks, batch_length=batch_length, quiet=quiet))
    event_loop.close()  # Close the event loop to free resources
    
    # Loop over database_convert to concat them into dataframe_maps
    if not quiet:
        print("")
    for i, df in enumerate(database_convert):
        if not quiet:
            print(f"Concatenating dataframes... {i + 1} of {len(database_convert)}" + " " * 50, end="\r")
        dataframe_maps = pd.concat([dataframe_maps, df], sort=False)
    if not quiet:
        print("")
    
    # Remove duplicate index values
    if remove_duplicates:
        dataframe_maps = dataframe_maps[~dataframe_maps.index.duplicated(keep='first')]
    
    return dataframe_maps
