import { useState } from "react";
import { Card, Container, Form, Button } from "react-bootstrap";
// import { getBackendURL } from "../config";
import { Formik } from "formik";
import * as Yup from "yup";
import { Schedule } from "./Schedule";

const schema = Yup.object().shape({
    amount: Yup.number().required("Amount is required!").min(1, "You must borrow at least $1.").max(1000000000, "We don't have that much money..."),
    term: Yup.number().required("Term is required!").min(1, "Term must be at least 1 year.").max(60, "Term can't be greater than 60 years."),
    rate: Yup.number().required("Rate is required!").min(0.1, "Rate must be greater than 0.1%").max(99.99, "Rate must be less than 100%."),
});
  
function AmortizationForm(props) {
    return (
      <Formik
        validationSchema={schema}
        onSubmit={(values, actions) => {
            const $ = window.$;
            $.ajax({
                url: 'http://localhost:8080/cashflow/calc-schedule',
                method: 'POST',
                dataType: 'json',
                headers: { 'Content-Type': 'application/json' },
                data: JSON.stringify({
                    loan_amount: values.amount, 
                    term: values.term, 
                    interest_rate: values.rate
                }),
                success: function(data) {
                    props.scheduleSetter(data);
                    props.valueSetter(values);
                }
            });
        }}
        initialValues={{}}
      >
        {({
          handleSubmit,
          handleChange,
          handleBlur,
          values,
          touched,
          isValid,
          errors,
        }) => (
            <Form noValidate onSubmit={handleSubmit}>
                <Form.Group className="mb-3" controlId="amount"> 
                    <Form.Label>
                        Loan Amount
                    </Form.Label>
                    <Form.Control 
                        value={values.amount} 
                        onChange={handleChange} 
                        name="amount" 
                        type="number" 
                        placeholder="Enter the amount that will be borrowed..." 
                        isInvalid={!!errors.amount} 
                    /> 
                    <Form.Control.Feedback type="invalid"> 
                        {errors.amount} 
                    </Form.Control.Feedback> 
                </Form.Group>
                <Form.Group className="mb-3" controlId="term"> 
                    <Form.Label>
                        Term in Years
                    </Form.Label>
                    <Form.Control 
                        value={values.term} 
                        onChange={handleChange} 
                        name="term" 
                        type="number" 
                        placeholder="Enter the term over which the loan will be repaid..." 
                        isInvalid={!!errors.term} 
                    /> 
                    <Form.Control.Feedback type="invalid"> 
                        {errors.term} 
                    </Form.Control.Feedback> 
                </Form.Group>
                <Form.Group className="mb-3" controlId="rate"> 
                    <Form.Label>
                        Annual Percentage Rate
                    </Form.Label>
                    <Form.Control 
                        value={values.rate} 
                        onChange={handleChange} 
                        name="rate" 
                        type="number" 
                        placeholder="Enter the interest rate precentage..." 
                        isInvalid={!!errors.rate} 
                    /> 
                    <Form.Control.Feedback type="invalid"> 
                        {errors.rate} 
                    </Form.Control.Feedback> 
                </Form.Group>
                <hr/>
                <Button 
                    className='mb-2' 
                    variant="primary" 
                    type="submit" 
                    disabled={!isValid}
                > 
                Calculate Schedule 
                </Button>
            </Form> 
        )}
      </Formik>
    );
}

export function Home(props) {

    const [schedule, scheduleSetter] = useState(null);
    const [values, valuesSetter] = useState(null);
    let scheduleContent;
    let valuesContent;
    if (schedule === null) {
        scheduleContent = <AmortizationForm scheduleSetter={scheduleSetter} valueSetter={valuesSetter}/>
        valuesContent= <></>;
    } else {
        scheduleContent = <Schedule data={schedule} />
        valuesContent = (
            <>
            <ul className="mb-2 list-group list-group-horizontal-sm">
                <li className="list-group-item list-group-item-light">Amount: <b>${values.amount}</b></li>
                <li className="list-group-item list-group-item-light">Term: <b>{values.term} years</b></li>
                <li className="list-group-item list-group-item-light">Rate: <b>{values.rate}%</b></li>
            </ul>
            </>
        )
    }
    return (
        <Container className='py-5'>
            <Card bg="light" className='shadow'>
                <Card.Body>
                    <Card.Title>🧮 Amortization Calculator</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">
                            Generate an Amortization Schedule based on Loan Amount, Term, and Rate.
                            <span className="float-end">
                                <Button 
                                    onClick={ () => { scheduleSetter(null) } }
                                    size="sm" 
                                    variant="light"
                                >
                                    ↩️ Reset
                                </Button>
                            </span>
                        </Card.Subtitle>
                        <hr/>
                        {valuesContent}
                        <Card.Text>
                            {scheduleContent}
                        </Card.Text>
                </Card.Body>
            </Card>
        </Container>
        
    );
}