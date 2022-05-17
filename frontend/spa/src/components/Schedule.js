import { useState } from "react";
import { Table, Button, ButtonGroup } from "react-bootstrap";

function getSchedule(uuid, offset, setter) {
    const $ = window.$;
    $.ajax({
        url: 'http://localhost:8080/cashflow/schedule',
        data: {
            uuid: uuid,
            offset: offset,
        },
        success: function(data) {
            setter(data);
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function RenderTableBody(props) {
    let rows = [];
    for (let i = 0; i < props.data.schedules.length; i++) {
        let row = (
            <tr>
                <th scope="row">{props.data.schedules[i].month}</th>
                <td>{props.data.schedules[i].starting_balance}</td>
                <td>{props.data.schedules[i].fixed_payment}</td>
                <td>{props.data.schedules[i].principal_payment}</td>
                <td>{props.data.schedules[i].interest_payment}</td>
                <td>{props.data.schedules[i].total_interest}</td>
                <td>{props.data.schedules[i].ending_balance}</td>
            </tr>
        )
        rows.push(row);
    }
    return (
        <tbody>
            {rows}
        </tbody>
    )
}

export function Schedule(props) {
    const [data, dataSetter] = useState(props.data);
    const nextPage = data.next_offset;
    const prevPage = data.prev_offset;
    const lastPage = data.total - 12;
    return (
        <div className="table-responsive">
            <Table striped hover size="sm">
            <thead>
                <tr>
                    <th>Month</th>
                    <th>Starting Balance</th>
                    <th>Fixed Payment</th>
                    <th>Principal Payment</th>
                    <th>Interest Payment</th>
                    <th>Total Interest</th>
                    <th>Ending Balance</th>
                </tr>
            </thead>
            <RenderTableBody data={data}/>
            </Table>
            <ButtonGroup size="sm">
                <Button onClick={() => getSchedule(data.uuid, 0, dataSetter)}>&lt;&lt;</Button>
                <Button onClick={() => getSchedule(data.uuid, prevPage, dataSetter)}>&lt;</Button>
                <Button onClick={() => getSchedule(data.uuid, nextPage, dataSetter)}>&gt;</Button>
                <Button onClick={() => getSchedule(data.uuid, lastPage, dataSetter)}>&gt;&gt;</Button>
            </ButtonGroup>
        </div>
    );
}