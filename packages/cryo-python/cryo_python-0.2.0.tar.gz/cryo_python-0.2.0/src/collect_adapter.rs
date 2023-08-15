use polars::prelude::*;
use pyo3::{exceptions::PyTypeError, prelude::*};
use pyo3_polars::PyDataFrame;

use cryo_cli::{parse_opts, Args};
use cryo_freeze::collect;

#[pyfunction(
    signature = (
        datatype,
        blocks = None,
        *,
        txs = None,
        align = false,
        reorg_buffer = 0,
        include_columns = None,
        exclude_columns = None,
        columns = None,
        hex = false,
        sort = None,
        rpc = None,
        network_name = None,
        requests_per_second = None,
        max_concurrent_requests = None,
        max_concurrent_chunks = None,
        dry = false,
        chunk_size = 1000,
        n_chunks = None,
        output_dir = ".".to_string(),
        file_suffix = None,
        overwrite = false,
        csv = false,
        json = false,
        row_group_size = None,
        n_row_groups = None,
        no_stats = false,
        compression = vec!["lz4".to_string()],
        report_dir = None,
        no_report = false,
        contract = None,
        topic0 = None,
        topic1 = None,
        topic2 = None,
        topic3 = None,
        inner_request_size = 1,
        no_verbose = false,
    )
)]
#[allow(clippy::too_many_arguments)]
pub fn _collect(
    py: Python<'_>,
    datatype: String,
    blocks: Option<Vec<String>>,
    txs: Option<Vec<String>>,
    align: bool,
    reorg_buffer: u64,
    include_columns: Option<Vec<String>>,
    exclude_columns: Option<Vec<String>>,
    columns: Option<Vec<String>>,
    hex: bool,
    sort: Option<Vec<String>>,
    rpc: Option<String>,
    network_name: Option<String>,
    requests_per_second: Option<u32>,
    max_concurrent_requests: Option<u64>,
    max_concurrent_chunks: Option<u64>,
    dry: bool,
    chunk_size: u64,
    n_chunks: Option<u64>,
    output_dir: String,
    file_suffix: Option<String>,
    overwrite: bool,
    csv: bool,
    json: bool,
    row_group_size: Option<usize>,
    n_row_groups: Option<usize>,
    no_stats: bool,
    compression: Vec<String>,
    report_dir: Option<String>,
    no_report: bool,
    contract: Option<String>,
    topic0: Option<String>,
    topic1: Option<String>,
    topic2: Option<String>,
    topic3: Option<String>,
    inner_request_size: u64,
    no_verbose: bool,
) -> PyResult<&PyAny> {
    let args = Args {
        datatype: vec![datatype],
        blocks,
        txs,
        align,
        reorg_buffer,
        include_columns,
        exclude_columns,
        columns,
        hex,
        sort,
        rpc,
        network_name,
        requests_per_second,
        max_concurrent_requests,
        max_concurrent_chunks,
        dry,
        chunk_size,
        n_chunks,
        output_dir,
        file_suffix,
        overwrite,
        csv,
        json,
        row_group_size,
        n_row_groups,
        no_stats,
        compression,
        report_dir,
        no_report,
        contract,
        topic0,
        topic1,
        topic2,
        topic3,
        inner_request_size,
        no_verbose,
    };

    pyo3_asyncio::tokio::future_into_py(py, async move {
        match run_collect(args).await {
            // Ok(df) => Ok(Python::with_gil(|py| py.None())),
            Ok(df) => Ok(PyDataFrame(df)),
            Err(_e) => Err(PyErr::new::<PyTypeError, _>("failed")),
        }
    })
}

async fn run_collect(args: Args) -> PolarsResult<DataFrame> {
    let (query, source, _sink) = match parse_opts(&args).await {
        Ok(opts) => opts,
        Err(_e) => panic!(),
    };
    match collect(query.into(), source).await {
        Ok(df) => Ok(df),
        Err(_e) => panic!(),
    }
}
