import { Nav, Navbar, Container } from "react-bootstrap";

export function AppNav(props) {
    return (
        <Navbar className="shadow navbar-dark" bg="dark" expand="lg">
        <Container>
            <Navbar.Brand href="/">Cashflow Challenge</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
            </Navbar.Collapse>
        </Container>
        </Navbar>
    );
}